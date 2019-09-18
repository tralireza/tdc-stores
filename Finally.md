![Shoei](https://github.com/AlirezaTorabi/tdc-stores/blob/master/Shoei.jpg)

* My favorite gif is at the top :-) and it's a jpg!
* I did the backend task.
* More time:
    * Improve model to keep two sorted lists for Name 
    and Latitude (fairly easy one so perhaps I should have done it.)
    or a map/hash table from the normalised postcodes to the 
    corresponding data.
    Since the main work is the iteration through the stores 
    to find 
    the ones within the radius of the search origin 
    creating a map/hash table to speed up the looking for 
    a specific postcode was not done, however "**/stores/\<postcode\>**" 
    was added with an iterative search to return the data for it. 
    The "**keys**" in the model speeds up the search for a postcode to 
    decide whether it's worth doing the full search however.
    * Get feedback regarding the main endpoint location. 
    At two minds about whether 
    "**/stores?p=\<postcode\>&r=\<radius\>**" was a better way forward.
    The mean reason not to do it was that the postcode must represent
    a store in the database and can't just be any postcode.
    * Would add more test coverage and include coverage 
    module in the project.
    * Add swagger (SwaggerHub) to document API endpoints.
    * Include SonarCube to do static analysis in the project.
    * Better CLI however I created API endpoints instead.
    * Add a React UI to the project (ie, the full stack task as well).
    * Running a full wsgi production server inside docker.
    * So many more... and hopefully fixing not too many bugs!
    
* I liked working on different aspect of the project. Data modeling, 
API interfacing with postcodes.io, concurrency design:
    * Very happy with the concurrency model and ReadWrite lock 
    that allows any number of reads/searches to happen and on 
    the fly updating 
    of the data while the reads/searches are still successful 
    and atomic transition to the updated version 
    of the data seamlessly to 
    readers and searchers.
    * Fairly late I noticed all my calculations were in Km and as such 
    I added a feature to allow both Km and miles radius search while
    adding "distance" data in the corresponding unit to the results.
    In fact by changing the EARTH_RADIUS constant to miles all could 
    have been turned into miles but that was after I had written
    all my test results in Km (which I didn't want to 
    change and covert manually :-) 
    I'm sorry I know it's just a times 1.6)
    * Containerising the package into Docker which makes running,
    distribution and deployment of it easier.
    * Uniform logging to console for development (even production).
    
* Improvements: 
    * I would say mentioning the unit of distance. I know it's miles
    by default (unfortunately my default was Km!) by I did all in Km and added both as a feature.
    Or perhaps you wanted both in the first place :-).
    * Ability to submit on github. I created a repo in github and uploaded my solution to it
    which allows better interaction and submission (however there could be
    some security or policy aspect to it).
