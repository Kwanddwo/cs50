#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    char* message = get_string("Message: ");

    int length = strlen(message);

    char binary[length][BITS_IN_BYTE];

    for (int i = 0; i < length; i++)
    {
        char temp = message[i];

        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            binary[i][BITS_IN_BYTE - j - 1] = temp % 2;
            temp /= 2;
        }
    }

    for (int i = 0; i < length; i++)
    {
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            print_bulb(binary[i][j]);
        }

        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
