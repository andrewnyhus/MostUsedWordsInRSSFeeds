
class Forms:

    def getHeader(self):
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <title>Most Common Words in RSS Feed Counter</title>
              <meta http-equiv="content-type" content="text/html; charset=utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
              <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

                <script type='text/javascript'>

                    function start(){
                        $('#newRowButton').on('click', function (e) {
                            addNewRow();
                            var indexFirstColLastRow = document.getElementsByClassName('text-center').length - 3;
                            fillRowWithCellNumStartingAt(indexFirstColLastRow);
                            attachListenerToButtons();

                        })
                    }

                    function replaceButtonAndDisplayChoices(btnIndex, servicesData, feedsByServiceData){

                        var serviceSelectorString = "#dropdownServices" + btnIndex;
                        var feedSelectorString = "#dropdownFeeds"+ btnIndex;

                        var dropdownFeed = $(feedSelectorString);
                        var dropdownService = $(serviceSelectorString);

                        $("#button"+btnIndex).css('visibility', 'hidden');
                        $(dropdownService).css('visibility', 'visible');
                        $(dropdownFeed).css('visibility', 'visible');
                        var getResultsBtn = document.getElementsByClassName("btn btn-success")[btnIndex];
                        $(getResultsBtn).css('visibility', 'visible');

                        for(i = 0; i < servicesData.length; i++){
                            var currentValueString = servicesData[i];
                            var currentOpt = '<option value="' + currentValueString + '">' + currentValueString;
                            currentOpt = $(currentOpt + "</option>");

                            $(dropdownService).append(currentOpt);
                        }

                        handleServiceDropDownChange($(dropdownService), feedsByServiceData, $(dropdownFeed));

                        $( serviceSelectorString ).change(function() {
                            handleServiceDropDownChange(this, feedsByServiceData, $(dropdownFeed));
                        });

                    }

                    function handleServiceDropDownChange(serviceDropDown, feedsData, feedDropDown){

                        var sddIndex = $(serviceDropDown).prop("selectedIndex");
                        handleFeedsDropDown(feedDropDown, feedsData[sddIndex]);

                    }

                    function handleFeedsDropDown(feedDropDown, feedData){
                        feedDropDown.html('');
                        for(i = 0; i < feedData.length; i++){
                            var currentOptionValue = feedData[i][1];
                            var currentOptionTitle = feedData[i][0];

                            var currentOption = '<option value="' +currentOptionValue+ '">' + currentOptionTitle;
                            currentOption = $(currentOption + "</option>");

                            $(feedDropDown).append(currentOption);

                        }
                    }

                    function addNewRow(){
                        var numOfRows = document.getElementsByClassName('rowOfFeeds').length;
                        var numOfCells = numOfRows*3;
                        var newRowString =   '<div class="rowOfFeeds" style="margin-top:20px;margin-bottom:20px;" ><div class="col-sm-4" style="background-color:rgb(109, 155, 186);"><div class = "text-center"></div></div><div class="col-sm-4" style="background-color:rgb(109, 155, 186);"><div class = "text-center"></div></div><div class="col-sm-4" style="background-color:rgb(109, 155, 186);"><div class = "text-center"></div></div></div>';

                        $('#grid-container').append(newRowString);
                    }

                    function attachListenerToButtons(){

                        var buttons = document.getElementsByClassName('btn btn-default btn-block-center');
                        for(i = 0; i < buttons.length; i++){
                            var button = buttons[i];

                            $(button).on('click', function(e){
                                $.ajax({
                                    type: "GET",
                                    url: "/getFeeds/",
                                    contentType: "application/json; charset=utf-8",
                                    data: { id: e.target.id },
                                    success: function(data) {
                                        jsonObject = JSON.parse(data);
                                        serviceNames = [];
                                        feedsByService = [];
                                        for(j = 0; j < jsonObject.RSS.length; j++){
                                            serviceNames[j] = jsonObject.RSS[j].id;
                                            feedsInCurrentService = [];
                                            for(k = 0; k < jsonObject.RSS[j].feeds.length; k++){
                                                currentFeed = [];
                                                currentFeed[0] = jsonObject.RSS[j].feeds[k].title;
                                                currentFeed[1] = jsonObject.RSS[j].feeds[k].url;
                                                feedsInCurrentService[k] = currentFeed;
                                            }
                                            feedsByService[j] = feedsInCurrentService;
                                        }

                                        var buttonNum = parseInt(e.target.id.substring(6));
                                        replaceButtonAndDisplayChoices(buttonNum, serviceNames, feedsByService);

                                    }
                                });

                            })

                        }

                    }

                    function generateAddFeedButtonWithIndex(index){
                        var btnString = '<button id="button'+ index +'" name="newFeedBtn" class="btn btn-default btn-block-center" >+ New Feed</button>';

                        return btnString ;
                    }

                    function convertRSSFeedUrlToAcceptableWildcard(feedURL){
                        var replacementForSlash = "$@$@";
                        var slashFreeURL;
                        slashFreeURL = feedURL.replace(/\//g, replacementForSlash);

                        return slashFreeURL;
                    }

                    function generateGetEntriesResultsButtonWithIndex(index){

                        var getResultsBtn = $('<button type="button" style="background-color:orange;" class="btn btn-success">Analyze RSS Entries</button>');
                        $(getResultsBtn).css('visibility', 'hidden');


                            $(getResultsBtn).on('click', function(e){
                                $.ajax({
                                    type: "GET",
                                    url: "/getResults/"+ convertRSSFeedUrlToAcceptableWildcard($("#dropdownFeeds"+index).val()) ,
                                    contentType: "application/json; charset=utf-8",
                                    data: { id: e.target.class },
                                    success: function(data) {
                                        var jsonObject = JSON.parse(data);
                                        var wordsObject = jsonObject.RSS[0].words;
                                        var resultsArray = [];
                                        for(i = 0; i < wordsObject.length; i++){
                                            //console.log(i+') word:'+ wordsObject[i].word + ':# times:' + wordsObject[i].occurrences);
                                            resultsArray[i] = '"' + wordsObject[i].word + '" appeared ' + wordsObject[i].occurrences + ' times.';
                                        }
                                        populateResultsListWithIndex(index, resultsArray);

                                    }
                                });

                            })

                            return getResultsBtn;

                    }

                    function fillRowWithCellNumStartingAt(beginningCellIndexOfRow){
                        var leftCellIndex = beginningCellIndexOfRow;
                        var middleCellIndex = beginningCellIndexOfRow + 1;
                        var rightCellIndex = beginningCellIndexOfRow + 2;

                        var i = 0;
                        $('.text-center').each(function(){
                            if(i == leftCellIndex || i == middleCellIndex || i == rightCellIndex){
                                var btn = generateAddFeedButtonWithIndex(i);

                                var dropdownServicesId = 'dropdownServices' + i;
                                var dropdownServices = $('<select id="'+dropdownServicesId+'" ></select>');
                                $(dropdownServices).css('visibility', 'hidden');

                                var dropdownFeedsId = 'dropdownFeeds' + i;
                                var dropdownFeeds = $('<select id="'+dropdownFeedsId+'" ></select>');
                                $(dropdownFeeds).css('visibility', 'hidden');

                                var resultsListId = 'resultsList' + i;
                                var resultsList = $('<textarea readonly id="'+resultsListId+'" cols = "40" rows="7"></textarea>');


                                $(this).append(btn);
                                $(this).append($("<br>"));
                                $(this).append(dropdownServices);
                                $(this).append($("<br>"));
                                $(this).append(dropdownFeeds);
                                $(this).append($("<br>"));
                                $(this).append($("<br>"));
                                $(this).append(generateGetEntriesResultsButtonWithIndex(i));
                                $(this).append($("<br>"));
                                $(this).append(resultsList);


                            }
                            i++;
                        });



                    }

                    function populateResultsListWithIndex(index, results){
                        var resultsListid = 'resultsList' + index;
                        var resultsList = $('#'+resultsListid);
                        var numCols = document.getElementById(resultsListid).cols;
                        var line = "";
                        for(i = 0; i < numCols; i++){
                            line = line + "-";
                        }

                        var resultString = '';
                        for(z = 0; z < results.length; z++){
                            resultString = resultString + results[z] + "\\n" + line + "\\n";

                        }

                        $(resultsList).val(resultString);

                    }


                </script>
              <style>
                body{
                    background-color:rgb(109, 155, 186);
                    color:white;
                }

                .jumbotron{
                    background-color:rgb(109, 155, 186);
                }

                textarea{
                    background-color:rgb(109, 155, 186);
                    color:white;
                }



              </style>
            </head>
        '''

    def getPageTitleHeader(self):
        return '''
            <div class="jumbotron">
                <p style = "margin-left:20px;" >To begin, please click on one of the buttons below that reads "+ New Feed"
                    Next, specify which feed you want to analyze, and then the results will be displayed of every word that occurs in the
                    feed more than once in the given entry set.
                </p>
            </div>

        '''

    '''def getButton(self):
        return
                <button type="button" class="btn btn-default btn-block-center" >+ New Feed</button>
               '''
