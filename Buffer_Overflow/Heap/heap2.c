#include <stdlib.h>
#include <stdio.h>
#include <string.h>

struct data{
	char name[64];
}
struct fp{
	int(*fp)();
}
void executeShell(){
	char *name[2];
	name[0] = "/bin/sh";
	name[1] = NULL;
	execve(name[0], name, NULL);
}
void Failed(){
	printf("You failed to exploit the heap\n");
}
int int main(int argc, char const *argv[])
{
	char *a, *b, *c;

	a = malloc(32);
	b = malloc(32);
	c = malloc(32);

	strcpy(a, argv[1]);
	strcpy(b, argv[2]);
	strcpy(c, argv[3]);

	free(c);
	free(b);
	free(a);

	printf("You failed\n");
}