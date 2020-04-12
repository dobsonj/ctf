
Ocean Boutique
400
Welcome to the Ocean Boutique. Last year, y'all enjoyed the Snake Boutique, but I wanted to move closer to the C and find sequels by the shore, so I opened a new boutique.

Your boss has directed you to purchase exactly 31337.42 of goods and keep the receipt. Don't forget to make sure it all fits in your suitcase!

nc ctf.umbccd.io 5400


Run it locally, see what happens.

kali@kali:~/Downloads$ ./ocean_boutique 
Welcome to the Ocean Boutique.
Last year, y'all enjoyed the Snake Boutique, but I wanted to move closer to
the C and find sequels by the shore, so I opened a new boutique.

Your boss has directed you to purchase exactly 31337.42 of goods and keep the
receipt. Don't forget to make sure it all fits in your suitcase!
Thank you for using our self checkout, enjoy your vacation!

Enter transaction.
fooooood
error

Decompile it with Ghidra. entry() calls into this function:

undefined8 FUN_00101143(void)
{
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  puts(
      "Welcome to the Ocean Boutique.\nLast year, y\'all enjoyed the Snake Boutique, but I wantedto move closer to\nthe C and find sequels by the shore, so I opened a new boutique.\n\nYourboss has directed you to purchase exactly 31337.42 of goods and keep the\nreceipt. Don\'tforget to make sure it all fits in your suitcase!\nThank you for using our self checkout,enjoy your vacation!\n"
      );
  FUN_00100dbb();
  FUN_001010db();
  if ((((DAT_003020b0 == '\0') || (DAT_003020b1 == '\0')) || (DAT_003020b4 != 0)) ||
     (DAT_003020b8 != 0x2fd12e)) {
    puts("Your boss is livid, you didn\'t follow his instructions. You\'re fired.");
    error();
  }
  else {
    if (DAT_003020c0 < 0x3e9) {
      FUN_00100bea();
    }
    else {
      puts(
          "You made it all the way to the airport, but your bags were too heavy. You are\nforced toleave an item behind. When you tell your boss the story, he signs you\nup for synergytraining to help you plan better. Whomp whomp."
          );
      error();
    }
  }
  return 0;
}

FUN_00100bea() will get the flag, so we know we want (DAT_003020c0 < 0x3e9):

void FUN_00100bea(void)
{
  char *local_20;
  size_t local_18;
  FILE *local_10;
  
  local_18 = 0;
  local_20 = (char *)0x0;
  local_10 = fopen("flag.txt","r");
  if (local_10 == (FILE *)0x0) {
    local_20 = strdup("DogeCTF{Flag is different on the server.}\n");
  }
  else {
    local_18 = 0;
    getline(&local_20,&local_18,local_10);
    fclose(local_10);
  }
  printf("%s",local_20);
  free(local_20);
  return;
}

But the first function we enter is this, which asks for the transaction:

void FUN_00100dbb(void)
{
  char local_38 [24];
  char *local_20;
  uint local_18;
  uint local_14;
  ulong local_10;
  
  puts("Enter transaction.");
  local_10 = 0;
  while( true ) {
    if (0xe < local_10) {
      error();
      return;
    }
    local_14 = 0;
    local_18 = 0;
    fgets(local_38,0x14,stdin);
    local_20 = strtok(local_38," ");
    if (local_20 == (char *)0x0) {
      error();
    }
    local_14 = atoi(local_20);
    local_20 = strtok((char *)0x0," ");
    if (local_20 == (char *)0x0) {
      error();
    }
    local_18 = atoi(local_20);
    FUN_00100d57((ulong)local_14,(ulong)local_18,(ulong)local_18);
    if (local_14 == 9) break;
    local_10 = local_10 + 1;
  }
  DAT_003020b1 = local_18 == 10;
  putchar(10);
  return;
}

That function takes two integers and pass them into:

void FUN_00100d57(undefined4 param_1,undefined4 param_2)
{
  undefined4 *puVar1;
  undefined *local_10;
  
  puVar1 = (undefined4 *)malloc(0x10);
  *puVar1 = param_1;
  puVar1[1] = param_2;
  local_10 = &DAT_003021b0;
  while (*(long *)(local_10 + 8) != 0) {
    local_10 = *(undefined **)(local_10 + 8);
  }
  *(undefined4 **)(local_10 + 8) = puVar1;
  return;
}

This takes the 2 inputs and stores them as key:value pairs.
It allocates 16 bytes to store param_1 and param_2.
Then it starts with &DAT_003021b0 and iterates through until it finds an empty slot to store the pointer.

9 for the first input will end the transaction:

    if (local_14 == 9) break;

And DAT_003020b1 will be non-zero only if the second input is 10:

  DAT_003020b1 = local_18 == 10;

The next function that gets called is:

void FUN_001010db(void)
{
  uint *local_10;
  
  puts(
      "Processing transaction. Hopefully you remembered to:\nPurchase, Total, Pay, and EndTransaction\n"
      );
  local_10 = (uint *)&DAT_003021b0;
  while (*(long *)(local_10 + 2) != 0) {
    local_10 = *(uint **)(local_10 + 2);
    FUN_00100f97((ulong)*local_10,(ulong)local_10[1],(ulong)local_10[1]);
  }
  if (DAT_003020b1 != '\0') {
    FUN_00100ceb();
  }
  return;
}

This iterates over the requests and passes them into FUN_00100f97(), which maps our first input to a set of functions:

void FUN_00100f97(undefined4 param_1,uint param_2)
{
  uint uVar1;
  
  uVar1 = DAT_003020bc;
  switch(param_1) {
  case 3:
    if (DAT_003020b0 != '\0') {
      error();
    }
    if ((int)param_2 < 0) {
      error();
    }
    FUN_00100f2a((ulong)param_2);
    uVar1 = DAT_003020bc;
    break;
  case 4:
    if (DAT_003020b0 != '\0') {
      error();
    }
    uVar1 = param_2;
    if ((int)param_2 < 0) {
      error();
      uVar1 = param_2;
    }
    break;
  default:
    error();
    uVar1 = DAT_003020bc;
    break;
  case 6:
    if (DAT_003020b0 != '\x01') {
      error();
    }
    if ((int)param_2 < 0) {
      error();
    }
    if (DAT_003020b4 < (int)param_2) {
      error();
    }
    DAT_003020b8 = param_2 + DAT_003020b8;
    DAT_003020b4 = DAT_003020b4 - param_2;
    uVar1 = DAT_003020bc;
    break;
  case 8:
    if (DAT_003020b0 != '\0') {
      error();
    }
    if (param_2 != 8) {
      error();
    }
    DAT_003020b0 = '\x01';
    uVar1 = DAT_003020bc;
    break;
  case 9:
    break;
  }
  DAT_003020bc = uVar1;
  return;
}

If our last line had a value of 10, FUN_001010db() also calls FUN_00100ceb(), which prints our receipt:

void FUN_00100ceb(void)
{
  uint *local_10;
  
  local_10 = (uint *)&DAT_003021c0;
  puts("Receipt");
  while (*(long *)(local_10 + 4) != 0) {
    local_10 = *(uint **)(local_10 + 4);
    printf("%d\t%s\n",(ulong)*local_10,*(undefined8 *)(*(long *)(local_10 + 2) + 8));
  }
  putchar(10);
  return;
}

So at this point, we know the last line should be "9 10"

kali@kali:~/Downloads$ echo "9 10" | ./ocean_boutique 
Welcome to the Ocean Boutique.
Last year, y'all enjoyed the Snake Boutique, but I wanted to move closer to
the C and find sequels by the shore, so I opened a new boutique.

Your boss has directed you to purchase exactly 31337.42 of goods and keep the
receipt. Don't forget to make sure it all fits in your suitcase!
Thank you for using our self checkout, enjoy your vacation!

Enter transaction.

Processing transaction. Hopefully you remembered to:
Purchase, Total, Pay, and End Transaction

Receipt

Your boss is livid, you didn't follow his instructions. You're fired.
error

Looking back at FUN_00100f97(), let's figure out what the other numbers do.

6 looks like a payment function:

  case 6:
    if (DAT_003020b0 != '\x01') {
      error();
    }
    if ((int)param_2 < 0) {
      error();
    }
    if (DAT_003020b4 < (int)param_2) {
      error();
    }
    DAT_003020b8 = param_2 + DAT_003020b8;
    DAT_003020b4 = DAT_003020b4 - param_2;
    uVar1 = DAT_003020bc;
    break;

But before you can run 6, you have to run 8 with a param of 8.
This must finalize the purchases.

  case 8:
    if (DAT_003020b0 != '\0') {
      error();
    }
    if (param_2 != 8) {
      error();
    }
    DAT_003020b0 = '\x01';
    uVar1 = DAT_003020bc;
    break;

and 4 must be updating the total. It's the only one that changes uVar1.

  case 4:
    if (DAT_003020b0 != '\0') {
      error();
    }
    uVar1 = param_2;
    if ((int)param_2 < 0) {
      error();
      uVar1 = param_2;
    }
    break;

which by process of elimination leaves 3 to add purchases:

  case 3:
    if (DAT_003020b0 != '\0') {
      error();
    }
    if ((int)param_2 < 0) {
      error();
    }
    FUN_00100f2a((ulong)param_2);
    uVar1 = DAT_003020bc;
    break;

void FUN_00100f2a(uint param_1)
{
  long lVar1;
  
  lVar1 = FUN_00100eb8((ulong)param_1);
  FUN_00100c84((ulong)DAT_003020bc,lVar1,lVar1);
  DAT_003020b4 = DAT_003020bc * *(int *)(lVar1 + 0x10) + DAT_003020b4;
  DAT_003020bc = 1;
  DAT_003020c0 = *(int *)(lVar1 + 0x14) + DAT_003020c0;
  return;
}

DAT_003020c0 is the number of items I guess, remember we want (DAT_003020c0 < 0x3e9). At most 1000 items.
And it's keeping a total at DAT_003020b4, and lVar1 is coming from here: 

undefined * FUN_00100eb8(int param_1)
{
  ulong local_10;
  
  local_10 = 0;
  while( true ) {
    if (5 < local_10) {
      error();
      return (undefined *)0;
    }
    if (*(int *)(&DAT_003020e0 + local_10 * 0x18) == param_1) break;
    local_10 = local_10 + 1;
  }
  return &DAT_003020e0 + local_10 * 0x18;
}

And then we add the transaction to a list:

void FUN_00100c84(undefined4 param_1,undefined8 param_2)
{
  undefined4 *puVar1;
  undefined *local_10;
  
  puVar1 = (undefined4 *)malloc(0x18);
  *puVar1 = param_1;
  *(undefined8 *)(puVar1 + 2) = param_2;
  local_10 = &DAT_003021c0;
  while (*(long *)(local_10 + 0x10) != 0) {
    local_10 = *(undefined **)(local_10 + 0x10);
  }
  *(undefined4 **)(local_10 + 0x10) = puVar1;
  return;
}


So right now my understanding is:

3 = purchase
4 = total
6 = pay
8 = finalize
9 = end transaction


kali@kali:~/Downloads$ ./ocean_boutique 
Welcome to the Ocean Boutique.
Last year, y'all enjoyed the Snake Boutique, but I wanted to move closer to
the C and find sequels by the shore, so I opened a new boutique.

Your boss has directed you to purchase exactly 31337.42 of goods and keep the
receipt. Don't forget to make sure it all fits in your suitcase!
Thank you for using our self checkout, enjoy your vacation!

Enter transaction.
3 9
3 10
4 19
8 8
6 19
9 10

Processing transaction. Hopefully you remembered to:
Purchase, Total, Pay, and End Transaction

error


Why did I get an error back instead of getting fired for not following directions?
Let's look back at the conditions we have to hit to get the flag:

  if ((((DAT_003020b0 == '\0') || (DAT_003020b1 == '\0')) || (DAT_003020b4 != 0)) ||
                 (DAT_003020b8 != 0x2fd12e)) {

	  if (DAT_003020c0 < 0x3e9) {

DAT_003020b0 is checkout (I think). It will be true by entering '8 8'. We can't add more purchases after that.

DAT_003020b1 is whether or not we want a receipt, it will be true if our last line is '9 10'

DAT_003020b4 is our balance, and it has to be zero when we're done.

DAT_003020b8 is our total that we have to hit:
    0x2FD12E = 3133742

DAT_003020c0 is the number of items we've purchased. It must be 1000 or less.
    0x3E9 = 1001


When we buy an item, the balance (DAT_003020b4) is updated here:

void FUN_00100f2a(uint param_1)
{
  long lVar1;
 
  lVar1 = FUN_00100eb8((ulong)param_1);
  FUN_00100c84((ulong)DAT_003020bc,lVar1,lVar1); 
  DAT_003020b4 = DAT_003020bc * *(int *)(lVar1 + 0x10) + DAT_003020b4;
  DAT_003020bc = 1;
  DAT_003020c0 = *(int *)(lVar1 + 0x14) + DAT_003020c0;
  return;
}

DAT_003020c0 just increments by 20 each time, so it's the weighted total of our items, where the weight is always 20.
That means we can order 50 items at most (1000 / 20)
Nope, I'm wrong, it's pointer arithmetic.

Both DAT_003020c0 and DAT_003020b4 are values based on lVar1 pointers.
lVar1 comes from calling this function:

undefined * FUN_00100eb8(int param_1)
{
  ulong local_10;

  local_10 = 0;
  while( true ) {
    if (5 < local_10) {
      error();
      return (undefined *)0;
    }
    if (*(int *)(&DAT_003020e0 + local_10 * 0x18) == param_1) break;
    local_10 = local_10 + 1;
  }
  return &DAT_003020e0 + local_10 * 0x18;
}

DAT_003020e0 is just some static data that it's looping over, 24 bytes at a time, for a max of 6 iterations (0 through 5).

                             DAT_003020e0                                    XREF[3]:     FUN_00100eb8:00100ee1(*), 
                                                                                          FUN_00100eb8:00100ee8(R), 
                                                                                          FUN_00100eb8:00100f01(*)  
        003020e0 01              ??         01h
        003020e1 00              ??         00h
        003020e2 00              ??         00h
        003020e3 00              ??         00h
        003020e4 00              ??         00h
        003020e5 00              ??         00h
        003020e6 00              ??         00h
        003020e7 00              ??         00h
        003020e8 c8              ??         C8h                                              ?  ->  001012c8
        003020e9 12              ??         12h
        003020ea 10              ??         10h
        003020eb 00              ??         00h
        003020ec 00              ??         00h
        003020ed 00              ??         00h
        003020ee 00              ??         00h
        003020ef 00              ??         00h
        003020f0 44              ??         44h    D
        003020f1 0a              ??         0Ah
        003020f2 02              ??         02h
        003020f3 00              ??         00h
        003020f4 08              ??         08h
        003020f5 00              ??         00h
        003020f6 00              ??         00h
        003020f7 00              ??         00h
        003020f8 1e              ??         1Eh
        003020f9 00              ??         00h
        003020fa 00              ??         00h
        003020fb 00              ??         00h
        003020fc 00              ??         00h
        003020fd 00              ??         00h
        003020fe 00              ??         00h
        003020ff 00              ??         00h

The first time we enter the loop:

    if (*(int *)(&DAT_003020e0 + local_10 * 0x18) == param_1) break;

local_10 will be zero, so the expected input value is 1 to break from the loop (the contents of *003020e0).
Here are the valid choices:

Item 0 (003020e0) = 0x1 (1)
Item 1 (003020f8) = 0x1e (30)
Item 2 (00302110) = 0x0a (10)
Item 3 (00302128) = 0x02 (2)
Item 4 (00302140) = 0x2a (42)
Item 5 (00302158) = 0x4d (77)

inputting any of those values for '3' will return a pointer to the value, stored in lVar1.

This next function is just maintaining the itemized receipt. I only see DAT_003021c0 referenced here and in the receipt function (FUN_00100ceb).

void FUN_00100c84(undefined4 param_1,undefined8 param_2)
{
  undefined4 *puVar1;
  undefined *local_10;
 
  puVar1 = (undefined4 *)malloc(0x18);
  *puVar1 = param_1;
  *(undefined8 *)(puVar1 + 2) = param_2;
  local_10 = &DAT_003021c0;
  while (*(long *)(local_10 + 0x10) != 0) {
    local_10 = *(undefined **)(local_10 + 0x10);
  }
  *(undefined4 **)(local_10 + 0x10) = puVar1;
  return;
}

So now that we have those pieces, back to this function:

void FUN_00100f2a(uint param_1)
{
  long lVar1;

  lVar1 = FUN_00100eb8((ulong)param_1);
  FUN_00100c84((ulong)DAT_003020bc,lVar1,lVar1);
  DAT_003020b4 = DAT_003020bc * *(int *)(lVar1 + 0x10) + DAT_003020b4;
  DAT_003020bc = 1;
  DAT_003020c0 = *(int *)(lVar1 + 0x14) + DAT_003020c0;
  return;
}

Item 0 (003020e0) = 0x1 (1)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 
Item 1 (003020f8) = 0x1e (30)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 
Item 2 (00302110) = 0x0a (10)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 
Item 3 (00302128) = 0x02 (2)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 
Item 4 (00302140) = 0x2a (42)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 
Item 5 (00302158) = 0x4d (77)
	(lVar1 + 0x10): 
	(lVar1 + 0x14): 

DAT_003020bc is only set by case 4:

  case 4:
    if (DAT_003020b0 != '\0') {
      error();
    }
    uVar1 = param_2;
    if ((int)param_2 < 0) {
      error();
      uVar1 = param_2;
    }
    break;
  ...
  }
  DAT_003020bc = uVar1;
  return;


I ran out of time on this one. I keep invalidating previous assumptions and my understanding is slowly improving, but I would probably need another half day to finish it at this rate. It's hard to keep all those random variable names straight.
I feel like there has to bee a more efficient way to go about this. A team member suggested angr.io or z3.

TODO: dedicate time to learning how to use angr.io and z3.

