# CS50Blog
CS50 Final Project (Web Track)

This is a blogging website build using Django, HTML (with Bootstrap 4), CSS and some JavaScript and jQuery.
The functionality of this website are:
- Allow registered users to create a new blog post. Like/dislike blog post and leave comments.
- Allow users to customise their profile. Choose and crop their desired profile image. Toggle between Light and Dark Mode.
- Number of blog posts and comments per page are paginated to reduce clutter and improve loading time. 
- Blog Posts, comments, likes/dislikes and profile settings are saved to the database. 
- To save space in the server, old profile picture are deleted automatically when the users uploads a new profile picture.
- Authors of the blog post/comments are able to update/delete their post/comments if desired. 

Currently, the profile images are stored in AWS S3 Buckets and the website is deployed using Heroku.

This Project is deployed to Heroku, try it out. Link: https://cs50-final-project-blog.herokuapp.com/

Inspiration and References used for this project are as follows:
- Main project inspired by Corey Schafer Django tutorials. Link: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
- Switch between light and dark mode. Link: https://www.youtube.com/watch?v=dOIU773P1iw
- Like and Dislike Button. Link: https://www.youtube.com/watch?v=PXqRPqDjDgc&t=1012s
- Leaving Comments within each Blog Post. Link: https://djangocentral.com/creating-comments-system-with-django/
- Delete old profile picture when the user uploads a new one. Link: https://pypi.org/project/django-cleanup/
- Crop profile picture. Link:https://simpleisbetterthancomplex.com/tutorial/2017/03/02/how-to-crop-images-in-a-django-application.html
- Pagination of blog pages and comments. Link: https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html

Future Improvements for the project can be implemented on the CS50 Sidebar:
- Showing the latest post since we have tracked the date/time the post is created on the database.
- Showing trending post based on likes/dislike ratio of each post.
- Add some announcements if the website has some important updates (such as T&C) to notify all users.
- Add a mini calender to show future events if any.

Please visit my Github to view my other projects. Link: https://github.com/Tingkai911 

Finally, a big thank you to the CS50 Team for this wonderful course.
