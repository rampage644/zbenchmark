#include <stdio.h>
#include <zvm.h>

#define size 1024

char buffer[size];
// pass filename as command line argument
// ./bench_2 <file_name>
int main(int argc, char** argv) 
{
#ifdef __native_client__
  zfork();
#endif
  if (argc < 2)
    return 1;
  FILE* f = fopen(argv[1], "r");
  size_t count = fread(buffer, size, 1, f);
  printf(buffer);
  fclose(f);
  return 0;
}