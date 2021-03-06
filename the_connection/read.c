#include <stdint.h>
#include <stdio.h>
#include <endian.h>

int main(int argc, char *argv[]) {
	int64_t len;
	char buf[1024 * 1024];
	fread(&len, 1, sizeof len, stdin);
	len = be64toh(len);
	fprintf(stderr, "len: %ld\n", len);
	fread(buf, 1, len, stdin);
	fwrite(buf, 1, len, stdout);
	return 0;
}
