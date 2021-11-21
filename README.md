# Final_Project


## Presentation

The chosen topic for this project deals with Food Access. The motivation behind this project is to identify and analyze communities that have a limited access to healthy and nutritious food. A food desert is defined as an area with limited access to affordable healthy food in contrast to an area with higher access to supermarkets and vegetable shops with organic foods, which is known as a food oasis. The United States Department of Agriculture estimates that there are over 23.5 million people living in food deserts. This means that the urban population is further than one mile to a supermarket  compared to ten miles in rural areas. These areas lack fresh foods and instead are surrounded by fast foods, which are high in sugar and saturated fats. Thus, these areas tend to suffer from obesity and diabetes. The data source we are using for this project comes from the United States Department of Agriculture Food Access Research Atlas 2019.  The data set contains census tract information for every county within the United States. The variables associated with each tract include median family income, poverty rate, population, percentage of population with a vehicle, and racial makeup of the location. One question we want to look at is to see if food access is related to income solely or if other factors contribute to the problem regarding food access. Does income affect the likelihood of being in a low access area considering some low access individuals are not low income. 




## Machine Learning Model

We plan to use a supervised machine learning model with the target variable being low access 1 to 10 (ie. 1 mile in urban vs. 10 miles in rural areas).
After looking at the results from a number of different models, we determined that our features were weak learners. Because of that we chose to use a random forest model. And we were able to slightly improve accuracy by boosting. While still not terribly accurate, it does perform better than the other models.

## Database

We designed a database using Postgres that filters and cleans the original data. We plan to join an additional data set to this database in upcoming segments for this project. 




