# Data Visualization Final Project
## Titanic: Casualties and Survivors


### Marc Wu
#### Submission Date: April 25, 2017



**1. Summary**
This data visualization depicts the casualty and survivor numbers of the sinking of the RMS Titanic.
It consists of an interactive stacked bar chart with focus on the socio-economic status of the passengers as indicated by the passenger class. Unsurprisingly, women and children had much higher chances of survival. However, this bias is far less distinct for the third class (the majority of passengers) which is quite surprising. 


**2. Design**
When I was doing my own exploratory analysis of the data set, it was unexpected for me to see such a difference of death rates across the passenger classes. Therefore, I decided to use a stacked bar chart with percentages, which is suitable for comparing the proportions of survivorship, along the dimension of passenger class.

Since I noticed that gender and age have a strong bias on survivorship, I wanted this information in my data visualization, too. Instead of having separate charts, I came up with the idea to add some form of interactivity by allowing the user to further breakdown the passenger class axis according to these categories. 

However, one immediate problem posed the breakdown according to age, since this feature has a relatively high range, creating a lot of sub-bars. I solved this by creating three distinct age groups: age unknown, children (< 18 years), and adults. Another problem was the fact that the sub-bars had no labels depicting the value of the breakdown category, e.g. "male", "female". The only way for the user to get this information was via tooltip. I improved the chart by adding labels for each stacked bar. At first it were unintentionally two per bar (one for perished and one for survived), which of course is redundant. Eventually, I was able with some help from Myles to reduce it to one label per bar, putting it at the bottom.

When looking at the sizes of each passenger class, it was evident that percentages have one drawback compared to absolute values: loss of information, i.e. you can derive from absolute numbers a percentage, but not vice versa. Hence, another option for the user was added to switch between both measures.

More effort was put into the improvement and simplification of the tooltip. Specifically, the pattern "feature: value" was replaced by just the value, which in my case was sufficient. 

After some more feedback, I implemented the following minor changes:
* change of "Child" to "Minor", because it has a clearer meaning. 
* added explanation why the data set is incomplete
* less opacity of the colors for a more aesthetic look

Lastly, I improved the commentary to include a strong message to make it clear, that my visualization is explanatory.


**3. Feedback**

**3.1 Ye-Sie K.**

What do you notice in the visualization?
* a lot more 3rd class ppl are part of this project. Does this reflect the overall structure from the total passenger number of 2,224?
* men from 3rd class represent more than 1/3 of the 891 ppl and they got only a survival ratio of ca. 15% which is a lot more crucial than for 1st and 2nd class men
* the lower the class the more children and the lower the survival ratio
* 1st and 2nd class have very few difference in the survival ratio but 3rd class ppl have a rapid drop in their survival ratio

What questions do you have about the data?
* What age is counted as adult and child?
* how many people were from 1st/ 2nd/ 3rd class from the 2,224 ppl in total from the titanic?
* how many passengers and how many crew member were included in this diagram?

What relationships do you notice?
* see answers to question no.1

What do you think is the main takeaway from this visualization?
* the less money you have the lower your chance to survive.
* ppl from lower class got bad cabines from which they couldnt flee fast enough to escape
* money is all that counts
 
Is there something you don’t understand in the graphic?
Any suggestions/improvements?
* it's fine. On mobile the switch of the menues does not work instantly, you have to click twice in order to switch for example between count an percentage.



**3.2 Minh B.**

What do you notice in the visualization?
* It's clearly structured.

What questions do you have about the data?
* I'm wondering why the data isn't complete with all passengers and also why the age of so many passengers is unknown.

What relationships do you notice?
* Female passengers are always priorised in every class but there are still many children in the third class which have died compared to the first and second.

What do you think is the main takeaway from this visualization?
* I like the gradually increasing columns in each class by going through the categories and also the dashed lines while hovering with the mouse over the columns.

Is there something you don’t understand in the graphic?
* Everything is easily understandable.

Any suggestions/improvements?
* Nothing that I could think of.



**3.3 Myles C.**

What do you notice in the visualization?

* Technically, it is excellent.
* The message isn't very clear. Even though it may seem like 'giving away the punchline', the commentary should include a strong message about your findings (because there is a clear theme in your visualization).
* There is gender and child bias in the survival rates, but this is far (far) less exaggerated for passengers in the 3rd class. It is amazing (shocking) to see it so clearly! And there is class bias.

What questions do you have about the data?

* None

What relationships do you notice?

* See above

What do you think is the main takeaway from this visualization?

* Humans are odd (compassionate, toward children (admirable), and uncompromising, when it comes to class (!?!?) ... at the same time).

Is there something you don’t understand in the graphic?

* No, it is very clear.

Any suggestions/improvements?

* The commentary needs to present as strong a message as the charts do (no matter how you describe the relationships in the commentary, it will not take way from the 'punch' of seeing the actual data). This will remove any possibility of a reviewer thinking that the visualization is Exploratory rather than Explanatory (the central theme of this project is that the visualization is explanatory).










**4. Resources**
* http://dimplejs.org/advanced_examples_viewer.html?id=advanced_bar_labels
* https://discussions.udacity.com/t/custom-tooltip-legend-order/189042/6
* https://discussions.udacity.com/t/aggregating-and-manipulating-data-using-dimple-js/184108
* https://discussions.udacity.com/t/project-feedback-help-request/242384
* http://stackoverflow.com/questions/32232518/how-to-change-the-order-of-grouped-bar-chart-in-dimple
* http://stackoverflow.com/questions/23291200/dimple-js-how-can-i-change-the-labels-of-a-chart-axis-without-changing-the-data
* http://stackoverflow.com/questions/18883675/d3-js-get-value-of-selected-option