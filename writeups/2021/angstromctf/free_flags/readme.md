# FREE FLAGS!!1!!

## Description

```
Clam was browsing armstrongctf.com when suddenly a popup appeared saying "GET YOUR FREE FLAGS HERE!!!" along with a download. Can you fill out the survey for free flags?

Find it on the shell server at /problems/2021/free_flags or over netcat at nc shell.actf.co 21703.

Author: aplet123
```

## Analysis

There is a `flag.txt` that we need to read by using `free_flags`

```
team8838@actf:/problems/2021/free_flags$ ls -l
total 24
-r--r----- 1 problem2021_free_flags problem2021_free_flags    45 Apr  2 13:14 flag.txt
-r-xr-sr-x 1 problem2021_free_flags problem2021_free_flags 16536 Apr  3 00:36 free_flags
team8838@actf:/problems/2021/free_flags$ cat flag.txt 
cat: flag.txt: Permission denied
team8838@actf:/problems/2021/free_flags$ ./free_flags 
Congratulations! You are the 1000th CTFer!!! Fill out this short survey to get FREE FLAGS!!!
What number am I thinking of???
2
Wrong >:((((
```

Decompile with Ghidra and look at main.

```c
ulong main(void)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  uint local_128;
  int local_124;
  int local_120;
  int local_11c;
  char local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0);
  puts(
      "Congratulations! You are the 1000th CTFer!!! Fill out this short survey to get FREE FLAGS!!!"
      );
  puts("What number am I thinking of???");
  __isoc99_scanf(0x1020e1,&local_11c);
  if (local_11c == 0x7a69) {
    puts("What two numbers am I thinking of???");
    __isoc99_scanf("%d %d",&local_120,&local_124);
    if ((local_120 + local_124 == 0x476) && (local_120 * local_124 == 0x49f59)) {
      puts("What animal am I thinking of???");
      __isoc99_scanf(" %256s",local_118);
      sVar2 = strcspn(local_118,"\n");
      local_118[sVar2] = '\0';
      iVar1 = strcmp(local_118,"banana");
      if (iVar1 == 0) {
        puts("Wow!!! Now I can sell your information to the Russian government!!!");
        puts("Oh yeah, here\'s the FREE FLAG:");
        print_flag();
        local_128 = 0;
      }
      else {
        puts("Wrong >:((((");
        local_128 = 1;
      }
    }
    else {
      puts("Wrong >:((((");
      local_128 = 1;
    }
  }
  else {
    puts("Wrong >:((((");
    local_128 = 1;
  }
  if (*(long *)(in_FS_OFFSET + 0x28) == local_10) {
    return (ulong)local_128;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

We just have to answer that series of questions correctly to get the flag.

The first one is `0x7a69` or `31337`.

The second one accepts two numbers, which add up to `0x476` (`1142`) and multiply to `0x49f59` (`302937`). These are small numbers, so a quick and dirty way to solve is:

```python
goalsum = 1142
goalprod = 302937
for i in range(1, 1141):
    x = i
    y = goalsum - i
    if x + y == goalsum and x * y == goalprod:
        print('Solved', x, y)
        break
```

```
kali@kali:~/Downloads/angstrom/free_flags$ python solve.py 
('Solved', 419, 723)
```

The third one is just `banana`.

## Solution

```
team8838@actf:/problems/2021/free_flags$ ./free_flags 
Congratulations! You are the 1000th CTFer!!! Fill out this short survey to get FREE FLAGS!!!
What number am I thinking of???
31337
What two numbers am I thinking of???
419 723
What animal am I thinking of???
banana
Wow!!! Now I can sell your information to the Russian government!!!
Oh yeah, here's the FREE FLAG:
actf{what_do_you_mean_bananas_arent_animals}
```

