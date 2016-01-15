
class Forms:

    def getHeader(self):
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <title>Most Common Words in RSS Feed Counter</title>
              <meta http-equiv="content-type" content="text/html; charset=utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
              <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
              <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

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


                        var getResultsBtn = $("#getResultsBtn"+btnIndex);

                        $(getResultsBtn).css('visibility', 'visible');

                        var serviceSelectorString = "#dropdownServices" + btnIndex;
                        var feedSelectorString = "#dropdownFeeds"+ btnIndex;

                        $("#button"+btnIndex).css('visibility', 'hidden');

                        $(serviceSelectorString).css('visibility', 'visible');
                        $(feedSelectorString).css('visibility', 'visible');

                        var enterRSSParagraphId = "enterRSSParagraph" + btnIndex;
                        var enterRSSInputId = "enterRSSInput" + btnIndex;

                        $("#"+enterRSSParagraphId).css('visibility', 'visible');
                        $("#"+enterRSSInputId).css('visibility', 'visible');

                        var dropdownWidth = $(serviceSelectorString).css('width');

                        for(i = 0; i < servicesData.length; i++){

                            var currentValueString = servicesData[i];

                            var currOptBtnStr = '<button type="button"  data-selected="false"  style="background-color:orange;color:white;" class="btn btn-success">'+currentValueString+'</button>';
                            var currOptBtn = $(currOptBtnStr);

                            currOptBtn.css('width', dropdownWidth);
                            currOptBtn.on('click', function(e){

                                var dropdownMenu = document.getElementById('dropdownServices'+ btnIndex).getElementsByClassName('dropdown-menu')[0];
                                var arrOfDropdownButtons = dropdownMenu.getElementsByTagName('button');

                                for(z = 0; z < arrOfDropdownButtons.length; z++){
                                    arrOfDropdownButtons[z].setAttribute('data-selected', 'false');
                                }
                                e.target.setAttribute('data-selected', 'true');

                                var indexOfTarget = 0;
                                for(y = 0; y < arrOfDropdownButtons.length; y++){
                                    if(arrOfDropdownButtons[y].getAttribute('data-selected') == true || arrOfDropdownButtons[y].getAttribute('data-selected') == 'true'){
                                        indexOfTarget = y;
                                    }
                                }


                                handleServiceDropDownChange(indexOfTarget, btnIndex, servicesData, feedsByServiceData);
                            })

                            var currentOpt = $('<li></li>');
                            currentOpt.append(currOptBtn);

                            $(serviceSelectorString).find(".dropdown-menu").append(currentOpt);
                        }

                    }

                    function handleServiceDropDownChange(selectedServiceIndex, dropIndex, servicesData, feedsData){
                        var serviceSelectorString = "#dropdownServices" + dropIndex;
                        var feedSelectorString = "#dropdownFeeds"+ dropIndex;

                        var serviceDropdownButton = $($(serviceSelectorString).find("button")[0]);
                        var indexOfSpanElementBeginning = (""+serviceDropdownButton.html()).search('<');

                         var newDropdownHTML;
                         var newTitleDropdown = servicesData[selectedServiceIndex];

                         if(indexOfSpanElementBeginning == -1){
                            //the span element is missing
                            newDropdownHTML = newTitleDropdown;
                         }else{
                            var spanString = serviceDropdownButton.html().substring(indexOfSpanElementBeginning);
                            newDropdownHTML = newTitleDropdown + spanString;
                         }

                        serviceDropdownButton.html(newDropdownHTML);


                        handleFeedsDropDown(dropIndex, feedsData[selectedServiceIndex]);

                    }

                    function handleFeedsDropDown(dropIndex, feedData){
                        var feedDropdown = $("#dropdownFeeds"+ dropIndex);

                        $(feedDropdown).find(".dropdown-menu").html('');
                        var dropdownWidth = $("#dropdownServices"+dropIndex).css('width');

                        for(i = 0; i < feedData.length; i++){
                            var currentBtnValue = feedData[i][1];
                            var currentBtnTitle = feedData[i][0];

                            var currOptBtnStr = '<button type="button" data-selected="false"  style="background-color:orange;color:white;" value="'+currentBtnValue+'" class="btn btn-success">'+currentBtnTitle+'</button>';
                            var currOptBtn = $(currOptBtnStr);

                            currOptBtn.css('width', dropdownWidth);


                            currOptBtn.on('click', function(e){

                                var dropdownMenu = document.getElementById('dropdownFeeds'+ dropIndex).getElementsByClassName('dropdown-menu')[0];
                                var arrOfDropdownButtons = dropdownMenu.getElementsByTagName('button');

                                for(z = 0; z < arrOfDropdownButtons.length; z++){
                                    arrOfDropdownButtons[z].setAttribute('data-selected', 'false');
                                }
                                e.target.setAttribute('data-selected', 'true');

                                var newTitleDropdown = e.target.textContent;

                                var feedDropdownButton = $($(feedDropdown).find("button")[0]);
                                var indexOfSpanElementBeginning = (""+feedDropdownButton.html()).search('<');

                                 var newDropdownHTML;

                                 if(indexOfSpanElementBeginning == -1){
                                    //the span element is missing
                                    newDropdownHTML = newTitleDropdown;
                                 }else{
                                    var spanString = feedDropdownButton.html().substring(indexOfSpanElementBeginning);
                                    newDropdownHTML = newTitleDropdown + spanString;
                                 }

                                $(feedDropdownButton).html(newDropdownHTML);

                            })

                            var currentOpt = $('<li></li>');
                            currentOpt.append(currOptBtn);

                            $(feedDropdown).find(".dropdown-menu").append(currentOpt);

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
                        var btnString = '<button id="button'+ index +'" name="newFeedBtn" style="background-color:orange;color:white;"  class="btn btn-default btn-block-center" >+ New Feed</button>';

                        return btnString ;
                    }

                    function convertRSSFeedUrlToAcceptableWildcard(feedURL){
                        var replacementForSlash = "$@$@";
                        var slashFreeURL;
                        slashFreeURL = feedURL.replace(/\//g, replacementForSlash);

                        return slashFreeURL;
                    }

                    function getProperURLAtIndex(index){

                        var properURLToAnalyze;


                        if($("#enterRSSInput"+index).val() != ""){
                            console.log($("#enterRSSInput"+index).val());
                            properURLToAnalyze = $("#enterRSSInput"+index).val();
                        }else{
                            console.log('b');
                            properURLToAnalyze = getValueOfFeedsDropdown(index);
                        }
                        return properURLToAnalyze;

                    }

                    function generateGetEntriesResultsButtonWithIndex(index){

                        var enterRSSParagraphId = "enterRSSParagraph" + index;
                        var enterRSSInputId = "enterRSSInput" + index;
                        var getResultsId = 'getResultsBtn' + index;

                        var getResultsBtn = $('<button type="button" style="background-color:orange;color:white;" id="'+getResultsId+'" class="btn btn-success">Analyze RSS Entries</button>');
                        $(getResultsBtn).css('visibility', 'hidden');


                            $(getResultsBtn).on('click', function(e){
                                console.log('heyrrr');
                                $.ajax({
                                    type: "GET",
                                    url: "/getResults/"+ convertRSSFeedUrlToAcceptableWildcard(getProperURLAtIndex(index)),
                                    contentType: "application/json; charset=utf-8",
                                    data: { id: e.target.class },
                                    success: function(data) {
                                        var jsonObject = JSON.parse(data);
                                        var wordsObject = jsonObject.RSS[0].words;
                                        var resultsArray = [];
                                        for(i = 0; i < wordsObject.length; i++){
                                            resultsArray[i] = '"' + wordsObject[i].word + '" appeared ' + wordsObject[i].occurrences + ' times.';
                                        }
                                        populateResultsListWithIndex(index, resultsArray);

                                    }
                                });

                            })

                            return getResultsBtn;

                    }

                    function getValueOfFeedsDropdown(index){
                        var dropdownMenu = document.getElementById('dropdownFeeds'+ index).getElementsByClassName('dropdown-menu')[0];
                        var arrOfDropdownButtons = dropdownMenu.getElementsByTagName('button');


                        for(i = 0; i < arrOfDropdownButtons.length; i++){
                            var currIsSelectedValue = arrOfDropdownButtons[i].getAttribute("data-selected");
                            if(currIsSelectedValue == true || currIsSelectedValue == 'true'){
                                return $(arrOfDropdownButtons[i]).val();
                            }
                        }
                        return;

                    }

                    function fillRowWithCellNumStartingAt(beginningCellIndexOfRow){
                        var leftCellIndex = beginningCellIndexOfRow;
                        var middleCellIndex = beginningCellIndexOfRow + 1;
                        var rightCellIndex = beginningCellIndexOfRow + 2;

                        var i = 0;
                        $('.text-center').each(function(){
                            if(i == leftCellIndex || i == middleCellIndex || i == rightCellIndex){
                                var btn = generateAddFeedButtonWithIndex(i);

                                var dropdownPartOne = '<div class="dropdown"  ><button class="btn btn-primary dropdown-toggle" style="background-color:orange;color:white;"  type="button" data-toggle="dropdown">';
                                var dropdownPartTwo = '<span class="caret"></span></button><ul style="background-color:orange; width:190px; max-height:115px; overflow:auto;"  class="dropdown-menu"></ul></div></div>';

                                var dropdownServicesId = 'dropdownServices' + i;
                                var dropdownServices = $('<div id="'+dropdownServicesId+'" class="container"  >' + dropdownPartOne + 'Choose One' + dropdownPartTwo);


                                var dropdownFeedsId = 'dropdownFeeds' + i;
                                var dropdownFeeds = $('<div id="'+dropdownFeedsId+'" class="container" >' + dropdownPartOne + 'Choose One' + dropdownPartTwo);

                                var resultsListId = 'resultsList' + i;
                                var resultsList = $('<textarea readonly id="'+resultsListId+'" cols = "40" rows="7"></textarea>');
                                $(resultsList).css('visibility', 'hidden');

                                $(this).append(btn);
                                $(this).append($("<br>"));
                                $(this).append(dropdownServices);
                                $(this).append($("<br>"));
                                $(this).append(dropdownFeeds);
                                $(this).append($("<br>"));

                                var enterRSSParagraphId = "enterRSSParagraph"+i;
                                var enterRSSInputId = "enterRSSInput"+i;

                                $(this).append($('<p id="'+enterRSSParagraphId+'">or enter link to RSS Feed:</p>'));
                                $(this).append($('<input type="text" id="'+enterRSSInputId+'">'));
                                $(this).append($("<br>"));
                                $(this).append($("<br>"));
                                $(this).append(generateGetEntriesResultsButtonWithIndex(i));
                                $(this).append($("<br>"));
                                $(this).append(resultsList);

                                var buttonWidth = $('#button' + i).css('width');
                                var dropdownWidth = (parseInt(buttonWidth.replace(/px/,""))+68)+"px";

                                $(dropdownFeeds).css('width', dropdownWidth);
                                $(dropdownFeeds).css('visibility', 'hidden');

                                $(dropdownServices).css('width', dropdownWidth);
                                $(dropdownServices).css('visibility', 'hidden');

                                var enterRSSParagraphId = "enterRSSParagraph" + i;
                                var enterRSSInputId = "enterRSSInput" + i;

                                $("#"+enterRSSParagraphId).css('visibility', 'hidden');
                                $("#"+enterRSSInputId).css('visibility', 'hidden');


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

                        $(resultsList).css('visibility', 'visible');


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

                .col-sm-4{
                    border:1px solid white;
                }

                input{
                    color:black;
                }

              </style>
            </head>
        '''


    def getPageTitleHeader(self):
        return '''
            <div class="jumbotron">
                <p style = "margin-left:20px;" >To begin, please click on one of the buttons below that reads "+ New Feed"
                    Next, specify which feed you want to analyze, and then the results will be displayed of every word that occurs in the
                    feed more than once in the given entry set.  If you would like to use a feed not shown in the drop down, make sure it is a RSS url.
                    If you want to choose a feed from the drop down menus, make sure that the text entry field for RSS urls
                    is empty.
                </p>
            </div>

        '''

    '''def getButton(self):
        return
                <button type="button" class="btn btn-default btn-block-center" >+ New Feed</button>
               '''
