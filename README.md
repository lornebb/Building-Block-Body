# Building-Block-Body

It's no secret that a key to a healthy life is to be active, and for many, the hardest part is figuring out where to start. Building Block Body allows you to put your own workout together in blocks, from a database of other users' favourite excersizes.

If you would like to get in touch about this project, head over to my github profile to get the details.

## User Experience

### Goals

The primary goal of this project is to allow users to create, view, store, arrange, and share workouts. Workouts are submitted as individual exercises, that are categorised in various ways to make putting a complete workout together easy - hopfully making getting started that little bit easier.

### Target User Goals

* Create and store your favourite excersises.
* Put together complete workouts from a list of all submitted individual excersises from entire user base.
* Have ones own library of submitted data and workout compliations that is editable.
* View data on smart phone / tablet / desktop.
* Have the ability to message the developer.
* Easy to use design.

### Developer Goals

* Collect a database of excersises.
* Open communication with users via in-site email.
* Generate useful analytics of data collected.

### User Stories

As a personal trainer that now needs to work remotely over video calls, Paul needs a place to digitalise her workouts to pass to clients. He is used to writing them out by hand and using it as a reference on face to face workouts, or then typing everything out to email ahead to each client every day.

As a casual exeriser, John would like to put together a workout without having to subscribe to an expensive subscription app on his phone. He would like to put together workouts and change elements as he likes on a weekly basis.

As a new years resolution, Ringo would like to start working out again regularly, but only remembers a handful of exersices from the old days. He would like to digitalise his collection of memory based workouts, cross reference them with workouts from other people and get started as quickly as possible!

### User Requirements/Expectations

#### **Requirements:**

* Visually appealing website and easy/familiar navigation.
* A safe and sensible collection and display of users data.
* Easy to use forms for excersise data input.
* Easy to use complete workout builder.

#### **Expectations:**

* Tips for new users.
* Tips for new-comers to excerise / how to put together a decent workout.
* Profile page with history of workouts.
* Ability to edit listings.

### Design Choices

#### Fonts

##### Heading-Font

##### Content-font

#### Icons

#### Colours

#### Base Styles

##### Colour Palette

##### Shadows

##### Transitions

#### Images

#### Background Images

## Wireframes

Adobe XD with Material Ui Kit expansion.

## Flowcharts

### Account Creation Flowchart

### Database Design

#### Data Storage Types

##### example collection

example excersie name | key in collection |target body area | difficulty | reps | etc
:-:|:-:|:-:|:-:|:-:|:-:
squat | _id | etc | etc | etc

##### Types Collection

##### Users Collection

##### etc collection

##### Schema link here

## Features

### Existing Features

 Feature 1 - allows users X to achieve Y, by having them fill out Z

* Account creation - Allows the user to log in securely, then create, edit or delete their items on the database.

* Collections - Allows users to create workouts by combining chosen excersises into one workout.

* ??? Featured exersise? or workout?

### Features Left to Implement

* More intricate submissions from users that can then be searchable and scalable.

* An 'in workout' mode, where, once a user has selected their workout, can work through it with live timers, rest timers, and completed boxes.

* Progression logging - where a user can track a history of what exercises have been completed and how they did. Eg. rep progression, speed progression etc.

* Video integration of exercise into application. So each excersise logged can also include an inline player or uploaded video of the workout. Will most likely also include review process here for user security. 

* Video integration to be saved privately for users tracking or filming their own progression for reference later on.

## Technologies Used

### Languages

* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)

* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)

* [JavaScript](https://www.w3schools.com/js/)

* [JSON](https://www.json.org/json-en.html)

* [Python](https://www.python.org/)

### Tools & Libraries

* [jQuery](https://jquery.com/)

* [Git](https://git-scm.com/)

* [Material Design](https://material-ui.com/)

* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

* [PyMongo](https://pymongo.readthedocs.io/en/stable/)

* [SASS/SCSS](https://sass-lang.com/)

* [Flask](https://flask.palletsprojects.com/)

* [Jinja](https://jinja.palletsprojects.com)

<!-- * <a href="https://fontawesome.com/icons?d=gallery">Font-Awesome</a> -->

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X