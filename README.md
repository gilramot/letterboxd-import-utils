# letterboxd-utils
This is a repository that includes files that change the format of export data from different services to the [Letterboxd import format](https://letterboxd.com/about/importing-data/).

### Netflix
[Netflix allows you to download watching history](https://help.netflix.com/node/101917), although the file format only has the title and date watches (no media type or anything else to identify the title). The file `titles.txt` contains regex patterns of non-movie titles to remove from the file, although it is very incomplete. Feel free to pull request with more non-movie regex patterns. Keep in mind, netflix keeps track of movies you started watching but haven't finished, so you should still be careful with importing.

### IMDb
[IMDb has a much more informative export format](https://www.wikihow.com/Export-Your-IMDb-Custom-Lists-to-a-CSV-File), which allows a very accurate import. You can also export your lists from IMDb to letterboxd. Just make sure you use the `--input` flag for the file name.

### Disney+
Disney+ currently **has no watch history feature**, which means I can't do anything about it until they add a feature of this kind.

### Other services
In [the letterboxd import data help page](https://letterboxd.com/about/importing-data/), they have many other great tools to import data to letterboxd.
