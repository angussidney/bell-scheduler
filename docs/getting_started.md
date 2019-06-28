# Getting Started
## Accessing the application
The application can be accessed from the web browser on your computer by entering the URL provided by your IT administrator. It is recommended that you use a modern browser such as Firefox or Chrome (rather than Internet Explorer) for the best user experience. If you aren't given any addresses, you can try one or more of the following:

 - [127.0.0.1:5000](127.0.0.1:5000) (if the application can be accessed from any computer on the local network)
 - [0.0.0.0:5000](0.0.0.0:5000) (if the application can only be accessed from the computer it is installed on)
 - If neither of these options work, ask your IT administrator for assistance.

## Interface tour
There are five main parts of the program: the dashboard, the bell schedule, templates, sounds, and user management. All of these can be easily accessed via the navigation bar at the top of the page.

### Dashboard
Here, you can quickly see an overview of the current status of the bells. The dashboard allows you to:
 - View the full bell schedule for today
 - View the a summary of the schedule for the whole week
 - Manually ring a bell

### Schedules
Custom schedules allow you to easily adjust the bell schedule for any day of your choosing. Custom schedules will completely override the default bell template for the day, meaning that the new schedule can be set up in nearly any configuration.

### Templates
Templates make the process of configuring custom schedules even easier, by giving you a base off which you can customise common schedules. Generally, templates don't have any effect by themselves; rather, a custom shedule should be created based on the template in order to have any effect.

Templates are also used to set the default bell schedule for each day of the week.

> ### ProTip: Choosing between custom schedules and templates
> Schedules and schedules can be a little bit confusing. However, their distinct purposes can generally be boiled down to three main usecases:
>  - If the bell schedule is only being changed for a once-off occasion, and you're not planning on using the same schedule ever again, then a **custom schedule** will suffice
>  - If you're planning to use the same bell schedule more than once, then it may be helpful to first **create a template**, and then **create custom schedules** based on the template
>  - If you want the default bell schedule to be changed permanently for a certain day of the week, then a **template** is the best way to go.

### Sounds
The application is designed to give you complete flexibility over what sounds are played as bells. This means that you don't need to be limited to a standard bell sound - instead, you could consider scheduling music, or PA announcements. All that you need is a `.wav` file.

### User Management
> Note: this feature is only avaliable to administrative users

From this part of the program, you can view all of the current registered users, add new users, change user roles, and request password resets. 


