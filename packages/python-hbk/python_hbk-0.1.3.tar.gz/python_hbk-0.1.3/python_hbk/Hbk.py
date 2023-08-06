import json
import logging
import mmap
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


class Hbk:
    __BYTES_BETWEEN_ADDRESSES = 656
    __START_OFFSET = 448
    __ADDRESS_OFFSET = 80
    __LENGTH_OFFSET = 208
    __ARRAY_COUNT_OFFSET = 336

    def __init__(self, filepath: str = None, fileno: int = None):
        """
        Initializes a new instance of the Hbk class.

        Args:
            filepath (str, optional): The path to the file to map in memory. If specified, the file is opened in binary mode
                and memory-mapped using the mmap module. Default is None.
            fileno (int, optional): The file descriptor of the file to map in memory. If specified, the file is memory-mapped
                using the mmap module. Default is None.

        Raises:
            ValueError: If neither filepath nor fileno is provided.
        """

        if filepath is not None:
            logger.debug(f"Trying to open {filepath}.")
            with Path(filepath).open("rb") as f:
                logger.info("Successfully opened.")
                self.mmap_data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        elif fileno is not None:
            self.mmap_data = mmap.mmap(fileno, 0, access=mmap.ACCESS_READ)
        else:
            raise ValueError("Either filepath or fileno must be provided.")
        self.filesize = len(self.mmap_data) // self.__BYTES_BETWEEN_ADDRESSES
        logger.debug(f"Found {self.filesize} entries.")

    def read_until_end_string(self, offset: int) -> str:
        """
        Reads bytes from a memory-mapped file starting at the given offset until a null byte is encountered or the end of the
        file is reached, and returns the bytes as a UTF-8 encoded string.

        Args:
            offset (int): The offset in bytes from the beginning of the memory-mapped file to start reading from.

        Returns:
            str: The bytes read from the file, decoded as a UTF-8 encoded string.
        """
        value = bytearray()
        self.mmap_data.seek(offset)
        while byte := self.mmap_data.read(1):
            if byte == b"\x00":
                break
            value.append(byte[0])
        return value.decode("utf-8")

    def get_bookmark_names(self):
        """
        A generator function that reads the names of bookmarks from the memory-mapped file and yields them one at a time.

        Yields:
            str: The name of a bookmark.
        """
        for i in range(self.filesize):
            bookmark_name = self.read_until_end_string(self.__START_OFFSET)
            self.__START_OFFSET += self.__BYTES_BETWEEN_ADDRESSES
            yield bookmark_name
        self.__START_OFFSET = 448

    def get_bookmarks(self):
        """
        A generator function that reads bookmarks from the memory-mapped file and yields their names, addresses, and lengths.

        Yields:
            Tuple[str, str, int]: A tuple containing the name, address, and length of a bookmark.
        """

        for i in range(self.filesize):
            bookmark_name = self.read_until_end_string(self.__START_OFFSET)
            bookmark_address = self.read_until_end_string(
                self.__START_OFFSET + self.__ADDRESS_OFFSET
            )
            bookmark_length = int(
                self.read_until_end_string(self.__START_OFFSET + self.__LENGTH_OFFSET),
                16,
            )
            bookmark_array_count = int(
                self.read_until_end_string(
                    self.__START_OFFSET + self.__ARRAY_COUNT_OFFSET
                ),
                16,
            )
            logger.debug(
                f"Reading entry #{i} {bookmark_name=} {bookmark_address=} {bookmark_length=} "
                f"{bookmark_array_count=}"
            )
            if bookmark_array_count > 1:
                logger.debug(
                    f"{bookmark_name} is an array of {bookmark_array_count} values"
                )
                for j in range(bookmark_array_count):
                    array_address = (
                        hex(int(bookmark_address, 16) + j * bookmark_length)
                        .upper()
                        .replace("X", "0")
                    )
                    logger.debug(f"Array {bookmark_name} [{j}] {array_address=}")
                    yield f"{bookmark_name} [{j}]", bookmark_address, bookmark_length
            else:
                yield bookmark_name, bookmark_address, bookmark_length
            self.__START_OFFSET += self.__BYTES_BETWEEN_ADDRESSES
        self.__START_OFFSET = 448

    def to_json(self):
        output_json = []
        for bookmark_name, bookmark_address, bookmark_length in self.get_bookmarks():
            output_json.append(
                {
                    "name": bookmark_name,
                    "address": bookmark_address,
                    "length": bookmark_length,
                }
            )
        return json.dumps(output_json, indent=2)

    def get_entries_count(self):
        return self.filesize


if __name__ == "__main__":
    pass
