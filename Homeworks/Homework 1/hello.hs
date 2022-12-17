-- Homework 1


-- Haskell Warmup 
-- Question 1 
largest :: String -> String -> String 
largest string1 string2 = 
  if length string1 >= length string2
    then string1
  else
    string2

-- Question 2
reflect :: Integer -> Integer 
reflect 0 = 0
reflect num
  | num < 0 = (-1) + reflect num+1
  | num > 0 = 1 + reflect num-1

-- Question 3, part a
all_factors :: Integer -> [Integer]
all_factors int = [x | x <- [1..int], int `mod` x == 0]

-- Question 3, part b
perfect_numbers = [x | x <- [1..], sum (init (all_factors x)) == x]

-- Question 5
count_occurrences :: [Integer] -> [Integer] -> Integer
count_occurrences [] _ = 1 
count_occurrences _ [] = 0
count_occurrences (x:xs) (y:ys)
  | x == y = count_occurrences xs ys + count_occurrences (x:xs) ys
  | otherwise = count_occurrences (x:xs) ys
