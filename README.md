# Scroller

[deployed here](https://adcott-scroller-60f1d268c506.herokuapp.com/)

## Overview
Scroller is a poorly-named blogging and social networking platform focussing on **text-based** interaction. Its goal is to move away from the image/video heavy direction most sites are going and focus on quick page load times while minimising visual distraction and facilitating easy interaction.

I have intentionally aimed for a "retro" website feel (if ~20 years could be considered such a thing) with lots of inspiration being taken from circa 2000 LiveJournal. I have opted against an algrithm-based sorting in favour of a simpler "new stuff is at the top" approach.

A conscious decision was made to avoid images, video or any other rich media. There is to my knowledge no binary data being transferred from the server at all. In order to avoid a "wall of text" feel, dynamically created SVG shapes are used as identifying icons for users and communities, allowing for easier reading and navigation.

## Technologies Used

I have opted to use the most recent (at time of development) versions of all software

- Django 5.1.4
- HTMX 2.0.4
- jdenticon 3.3.0 (SVG patterns)
- Markdown & Bleach for minimal text styling
- \+ various django helper modules (seen in requirements.txt)

## UX Design Process

 User stories are paraphrased in the [GitHub Projects Kanban Board](https://github.com/users/james-adcott-edu/projects/6).

**Design Rationale:**
  - The layout is intentionally kept simple and unintrusive.
  - A mid-dark grey was chosen for the background colour to emphasise reability.
  - Standard browser fonts were kept as they are by default very legible
  - No images, different font sizes or inconsisten spacing is allowed in user input in order to maximise readability

## Key Features

1. **User Authentication** -- users are able to create accounts, securely login, delete account if required
2. **Community Management** -- users can create their own communities and post entries into them, or join other people's communities.
3. **Post Management** -- posts can be created, read, updated and deleted. Posts may contain a limited amount of styling in the form of either Markdown or HTML
4. **Comments** -- There is a threaded comment section below each post. Posting a comment does not refresh the whole page, instead it is built dynamically. Comments may be edited and deleted by authors and site admins.
5. **Blogging** -- users may have posts on their profile acting as a blog.
6. **Subscriptions** -- users may subscribe to communities or individual users' blogs. These posts are consolidated into a feed on the home page.
7. **auto-generated user icons** -- in the absence of images on the site, users can be identified by distinct SVG patterns associated with their username
8. **Dynamic updates** -- things like posting comments or subscribing to users/communities utilise HTMX and thus are done without the need for a page refresh.


**Inclusivity Notes** -- Designed to be very compatible with screen readers from the ground up. No images means no alt texts, etc.

## Deployment
- **Platform:** Heroku
- **High-Level Deployment Steps:** 
  1. Clone the repository
  2. Set up the Heroku environment with a PostgreSQL database.
  3. Configure SECRET_KEY and DATABASE_URL environment variables
  4. Deploy using Heroku with GitHub integration.

## AI Implementation and Orchestration

In previous projects I have opted for minimal AI involvement, however in the spirit of the course I decided to attempt to fully embrace it. My usual environment of Vim and inline AI code completion was swapped for VSCode and full-on AI pair programming via Copilot.

- **Code Creation:** 
  - I tried to give Copilot the opportunity of writing most of the code at some point. I quickly learned the importance of clear prompting. I have ended up having to rewrite the bulk of what was supplied as it has a clear tendancy towards being verbose and producing redundant duplicate code. I found asking the AI to improve the code immediately with prompts like "is that the best you can do?" to be suprisingly effective.

- **Debugging:** 
  - I found myself debugging the AI code more than the other way around. I did find it useful for problems like "you forgot to include the class at the top of the file" type things.
  - Pasting errors into the chat field is a nice way of locating problems though.

- **Performance and UX Optimization:** 
  - I asked Copiot to handle the responsive styling for screens over a size. I produced a simple CSS media query that I ended up using the bulk of.

- **Automated Unit Testing:**
  - I found Copilot reasonably adept at writing simple unit tests for forms/models, only requiring minimal changes.

### Overall Impact:
Overall I wouldn't say AI's impact has been transformative. It has a clear tendancy to hallucinate, make up uneeded functions, randomly change variable names and the like and so requires significant monitoring before any code is allowed to be committed.

For things like simple unit tests it has been useful, but for other things I have found that the time taken babysitting the output outweighs the time save by having the machine write it.


## Testing Summary
- **Manual Testing:**
  - **Devices and Browsers Tested:** Linux Chromium and Firefox
  - **Assistive Technologies:** Tested using Lighthouse in the Developer Tools.
  - **Features Tested:** CRUD operations, user authentication, responsive design.
  - **Results:** All critical features worked as expected.
- **Automated Testing:**
  - Tools Used: Django TestCase, GitHub Copilot.
  - Features Covered: CRUD operations, user authentication.

### Code Validation

- Passes CSS Validator
- Passes HTML Validator with the exception of `hx-headers` attribute on body (required for HTMX)
- Lighthouse Scores:
  - 95 Performance
  - 92 Accessibility
  - 100 Best Practices
  - 100 SEO

## Future Enhancements
- I have left several 'could-have's in the Kanban board's To-do section. Highest priority of those is likely the pagination/infinite scrolling feature as this is where the name idea came from.
