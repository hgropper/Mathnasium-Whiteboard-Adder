# Mathnasium-Whiteboard-Adder
During the beginning of the pandemic where I worked at Mathnasium, a math learning center, transitioned half online and half in person. I knew that this sudden transition would contribute a lot of stress and extra work in our workplace. So, I took it the initiative myself to automate a very tedious task to save tons of time!

## The task
Give access to all Mathnasium employees each student's whiteboard.

## Why was this important?
Everytime we wanted to work online with a student we had to load up their whiteboard (worksheet). 
Each whiteboard contains unique data about who can access it.
Whiteboards are constantly created, which means there must be continuing process that grants access to these whiteboards.  

## Problem!
RESTRICTION: Only one Mathnasium employee can be given access to one whiteboard at a time.
Impacts: This was a massive time waster! Someone would have to spend hours at a time everyday granting access to each student's whiteboard!

# Solution
Utilizing the requests module from python I can analyze the HTTP requests from https://conexed.com/ and automate this process. 


