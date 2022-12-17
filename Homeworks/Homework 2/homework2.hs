-- Homework 2

-- Question 1, part a
scale_nums :: [Integer] -> Integer -> [Integer]
scale_nums intList factor = map (\x -> x * factor) intList

-- Question 1, part b
only_odds :: [[Integer]] -> [[Integer]]
only_odds list = filter (all (\x -> x `mod` 2 /= 0)) list

-- from Homework 1
largest :: String -> String -> String 
largest first second = 
    if length first >= length second then first else second

-- Question 1, part c
largest_in_list :: [String] -> String
largest_in_list str_list = foldl largest "" str_list



-- Question 2, part a
count_if :: (a -> Bool) -> [a] -> Int
count_if pred [] = 0 -- if list is empty, return 0
count_if pred (x:xs) = 
    if pred x == True
        then (count_if pred xs) + 1
    else
        count_if pred xs

-- Question 2, part b
count_if_with_filter :: (a -> Bool) -> [a] -> Int
count_if_with_filter pred list = length (filter pred list)

-- Question 2, part c
-- count_if_with_foldl :: (a -> Bool) -> [a] -> Int
-- count_if_with_foldl pred list = if pred x then acc + 1 else acc 


-- Question 3, part c

-- Question 6, part g
data InstagramUser = Influencer [String] [InstagramUser] | Normie
