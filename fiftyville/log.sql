-- Keep a log of any SQL queries you execute as you solve the mystery.


-- Get database layout
.schema


-- Check crime_scene_report for description on the theft of the duck:
SELECT description FROM crime_scene_reports
WHERE street = "Humphrey Street"
AND year = 2021 AND month = 7 AND day = 28
AND description LIKE "%duck%";

/* Output: | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. | */


-- Check interviews table for the 3 interviews that mention the bakery:
SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

 /* Output: | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. | */


-- Check bakery_security_logs for license_plate on time of culprit leaving the crime scene:
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
AND activity = "exit";

/* Output:
+---------------+
| license_plate |
+---------------+
| 5P2BI95       |
| 94KL13X       |
| 6P58WS2       |
| 4328GD8       |
| G412CB7       |
| L93JTIZ       |
| 322W7JE       |
| 0NTHK55       |
+---------------+
*/


-- Check atm records for culprit's account number because of his withdrawal at Leggett Street on day of crime:
SELECT account_number FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

/* Output:
+----------------+
| account_number |
+----------------+
| 28500762       |
| 28296815       |
| 76054385       |
| 49610011       |
| 16153065       |
| 25506511       |
| 81061156       |
| 26013199       |
+----------------+
*/


-- Get the person_ids associated with these bank accounts:
SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28
        AND atm_location = "Leggett Street"
        AND transaction_type = "withdraw");

/* Output:
+-----------+
| person_id |
+-----------+
| 686048    |
| 514354    |
| 458378    |
| 395717    |
| 396669    |
| 467400    |
| 449774    |
| 438727    |
+-----------+
*/


-- Check call records for culprit's phone number from calls that heppened the day of the crime where the duration was less than a minute:
SELECT caller FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND duration < 60;

/* Output:
+----------------+
|     caller     |
+----------------+
| (130) 555-0289 |
| (499) 555-9472 |
| (367) 555-5533 |
| (499) 555-9472 |
| (286) 555-6063 |
| (770) 555-1861 |
| (031) 555-6622 |
| (826) 555-1652 |
| (338) 555-6650 |
+----------------+
*/


-- Check passengers for passports of people aboard earliest flight of July 29th:
SELECT passport_number FROM passengers WHERE flight_id =
    (SELECT id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29
    AND origin_airport_id =
        (SELECT id FROM airports WHERE city = "Fiftyville")
        ORDER BY hour, minute LIMIT 1);

/* Output:
+-----------------+
| passport_number |
+-----------------+
| 7214083635      |
| 1695452385      |
| 5773159633      |
| 1540955065      |
| 8294398571      |
| 1988161715      |
| 9878712108      |
| 8496433585      |
+-----------------+
*/


-- We can check for the culprit's name now:
SELECT name FROM people WHERE id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
        (SELECT account_number FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28
            AND atm_location = "Leggett Street"
            AND transaction_type = "withdraw"))

AND phone_number IN
    (SELECT caller FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28
        AND duration < 60)

AND passport_number IN
    (SELECT passport_number FROM passengers WHERE flight_id =
        (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29
            AND origin_airport_id =
                (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour, minute LIMIT 1))

AND license_plate IN
    (SELECT license_plate FROM bakery_security_logs WHERE
        year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
        AND activity = "exit");

/* Output:
+-------+
| name  |
+-------+
| Bruce |
+-------+
*/

-- Knowing which flight Bruce took we can see where he escaped to:
SELECT city FROM airports WHERE id =
    (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29
        AND origin_airport_id =
            (SELECT id FROM airports WHERE city = "Fiftyville")
        ORDER BY hour, minute LIMIT 1);

/* Output:
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+
*/

-- We know Bruce called his accomplice so let's check for the accomplice's phone number:
SELECT receiver FROM phone_calls WHERE caller =
    (SELECT phone_number FROM people WHERE name = "Bruce")
    AND year = 2021 AND month = 7 AND day = 28
    AND duration < 60;

/* Output:
+----------------+
|    receiver    |
+----------------+
| (375) 555-8161 |
+----------------+
*/

-- Let's check the people table for this number:

SELECT name FROM people WHERE phone_number =
    (SELECT receiver FROM phone_calls WHERE caller =
        (SELECT phone_number FROM people WHERE name = "Bruce")
        AND year = 2021 AND month = 7 AND day = 28
        AND duration < 60);

/* Output:
+-------+
| name  |
+-------+
| Robin |
+-------+
*/

-- Ladies and gentlemen, we got 'em