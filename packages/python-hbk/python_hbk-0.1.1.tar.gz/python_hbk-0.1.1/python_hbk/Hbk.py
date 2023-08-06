from pathlib import Path
import mmap
import ujson
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


class Hbk:
    BYTES_BETWEEN_ADDRESSES = 656
    START_OFFSET = 448
    ADDRESS_OFFSET = 80
    LENGTH_OFFSET = 208
    ARRAY_COUNT_OFFSET = 336

    def __init__(self, filepath: str = None, fileno: int = None):
        if filepath is not None:
            self.filepath = Path(filepath)
            logger.debug(f"Trying to open {self.filepath}.")
            with self.filepath.open("rb") as f:
                logger.info("Successfully opened.")
                self.mmap_data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        elif fileno is not None:
            self.mmap_data = mmap.mmap(fileno, 0, access=mmap.ACCESS_READ)
        else:
            raise ValueError("Either filepath or fileno must be provided.")
        self.filesize = len(self.mmap_data) // self.BYTES_BETWEEN_ADDRESSES
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
            name = self.read_until_end_string(self.START_OFFSET)
            self.START_OFFSET += self.BYTES_BETWEEN_ADDRESSES
            yield name
        self.START_OFFSET = 448

    def get_bookmarks(self):
        """
        A generator function that reads bookmarks from the memory-mapped file and yields their names, addresses, and lengths.

        Yields:
            Tuple[str, str, int]: A tuple containing the name, address, and length of a bookmark.
        """

        for i in range(self.filesize):
            bookmark_name = self.read_until_end_string(self.START_OFFSET)
            bookmark_address = self.read_until_end_string(
                self.START_OFFSET + self.ADDRESS_OFFSET
            )
            bookmark_length = int(
                self.read_until_end_string(self.START_OFFSET + self.LENGTH_OFFSET), 16
            )
            bookmark_array_count = int(
                self.read_until_end_string(self.START_OFFSET + self.ARRAY_COUNT_OFFSET),
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
            self.START_OFFSET += self.BYTES_BETWEEN_ADDRESSES
        self.START_OFFSET = 448

    def to_json(self):
        output_json = []
        for name, address, length in self.get_bookmarks():
            output_json.append({"name": name, "address": address, "length": length})
        return ujson.dumps(output_json, indent=2)

    def get_entries_count(self):
        return self.filesize


if __name__ == "__main__":
    hbk = Hbk(filepath="test.hbk")
    out_json = hbk.to_json()
    print(out_json)
    # for name, address, length in hbk.get_bookmarks():
    #     print(name, address, length)
