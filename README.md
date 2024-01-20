**User Manual**

**Project Name: AGENT BASED FIND POPULARITY OF MUSIC WITH DATA ACQUISITION**

**SOFTWARE**

_1. 201805032 – Ardıl Silan Aydın_

_2. 201805016 – Beril Kartal_

_3. 201805060 – Elif Yılmaz_

_4. 201805017 – Neslihan Özdil_

_5. 201805045 – Orhan Gazi Barak_

_6. 221805078 – Suat Ayhan_

In our program users can upload their songs’ lyrics, sounds and musics. So, they can see their song will be popular or not. We prepared this document for users how to use our program.

Firstly, in main page users can sign in to program as an user or an admin. Probably, you will be user so, you must be sign in as an user.

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps1.png) 

Users can sign in to the program with this button. Then, they will see this page.

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps2.png) 

User can click these three button according to what want to upload to the program. These three button opens same page for users’ upload.

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps3.png) 

User can select their file with marked with red color content. Then, upload to program their file with upload button.

As we mentinoned above, some users can sign in as admin with this button.

 ![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps4.png)

Admins can see uploaded user files and programs’ acquisition files from Internet but we will code this feature in spring semester. So, if you are an admin you can login with your username and password.

Username = admin

Password = admin123

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps5.jpg) 

When you login as an admin you will redirected our data page. The collected data will appear on this page. You will see blank page first seconds but you must not exit from page. Data will appear. You can watch the process from your terminal.

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps6.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps7.jpg) 

When the program finish collect the from Spotify page will seem this:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps8.jpg) 

**Development Manual**

In our program users can upload their songs’ lyrics, sounds and musics. So, they can see their song will be popular or not. We prepared this document for developers how to we develop this program.

Firstly we got some data from Spotify, Musixmatch and Youtube about this subject.

We got track name, artist, artist uri, artist popularity, artist genres, track duration (ms), relase date, track popularity, dancebility, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, type, track id, uri, track_href, analysis_url, duration_ms, time_signature, and lyrics from Spotify and Musixmatch with these codes:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps9.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps10.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps11.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps12.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps13.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps14.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps15.jpg) 

Then, we got mp3 formats these songs’ from youtube manually.

Lastly, we developed our website fort his project. We used Python Flask for backend and HTML/CSS for frontend.

Our backend codes:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps16.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps17.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps18.jpg) 

Our main page’s html codes:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps19.jpg)   

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps20.jpg) 

Our upload page’s html codes:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps21.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps22.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps23.jpg) 

Our admin page’s html codes:

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps24.jpg) 

![](file:///C:\Users\ORHANG~1\AppData\Local\Temp\ksohtml7280\wps25.jpg) 

In our project users can upload their songs’ files for now. We will develop other features at future.