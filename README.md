# fax-console-automation

A 5-week "0 knowledge to Production" Python, Selenium/webdriver project.

Began: March 2018
Deployed: April 2018

Prior to this project, I had never written Python and had no experience with Selenium. Over the course of 5 weeks, I learned enough Python to be dangerous and enough Selenium to complete the project. Management decided it was "good enough" to test and then deploy to Prod. After being deployed, it removed the need for Tier 1 Support to devote time and people to performing this task.

Aside from the occasional tweak due to changes with Fax Vendors, as of November 2022, it was still dutifully performing its task.

## Project Goal

This project was built with the intention of automating a web interface. Prior to its creation, a user would need to log in to this web interface, review a prescription that failed to transmit via fax for various reasons (either due to an error on the Company side or issues with the fax vendor), determine if the prescription should be marked undeliverable or queued for refax, and then take the appropriate action. The user was typically tasked to review the 5 "regions" the Company every 30 minutes.

The goal of the project was to automate the entire process.
