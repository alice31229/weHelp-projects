// hover tooltip conditionally based on ellipsis

// Task 3
// photo data show in the picture div
let dataLength = 0;
let loadTimes = 0;
let stitles = [];
let imgs = [];

let data_url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1';
    
// get data through fetch from data_url
fetch(data_url)
.then(function (response){
    return response.json();
})
.then(function (result){
    for (let spot in result.data.results){
        stitles.push(result.data.results[spot].stitle);
        imgs.push("https" +result.data.results[spot].filelist.split("https")[1]);
        
    };
    dataLength = result.data.count - 1;
    
    // three small and the following first ten pictures 
    //document.addEventListener("DOMContentLoaded", function (e) {
    let first13Stitle = stitles.slice(0, 13);
    let first13Img = imgs.slice(0, 13);

    const pictureI = document.querySelector('.pictureI');
    const pictureII = document.querySelector('.pictureII');

    for (let i = 0; i <= 12; i++){
        if (i <= 2){
            let divPIinner = document.createElement('div');
            let imgPInner = document.createElement('img');
            let stitlePInner = document.createElement('div');

            pictureI.appendChild(divPIinner);
            divPIinner.appendChild(imgPInner);
            divPIinner.appendChild(stitlePInner);

            imgPInner.src = first13Img[i];
            stitlePInner.textContent = first13Stitle[i];
            divPIinner.className = 'pIinner';
            stitlePInner.className = 'backColor';
            if (i < 2){
                divPIinner.setAttribute('id', 'pIinner_1_2')
            }else{
                divPIinner.setAttribute('id', 'pIinner_1')
            };
            

        }else{
            let divC_pIIinner_1_3 = document.createElement('div');
            let imgSpot = document.createElement('img'); // img append
            let divOverlayS = document.createElement('div');
            let imgStar = document.createElement('img');
            let divOverlayT = document.createElement('div'); // stitle append
            //let spanFullText = document.createElement('span'); // for ellipsis hover show full text

            divOverlayT.className = 'overlayT';
            //spanFullText.className = 'tooltiptext';
            divOverlayT.textContent = first13Stitle[i];
            //spanFullText.textContent = first13Stitle[i];
            imgSpot.src = first13Img[i];
            imgStar.src = 'star_icon.png';
            divOverlayS.className = 'overlayS';

            pictureII.appendChild(divC_pIIinner_1_3);
            divC_pIIinner_1_3.appendChild(imgSpot);
            divC_pIIinner_1_3.appendChild(divOverlayS);
            divOverlayS.appendChild(imgStar);
            divC_pIIinner_1_3.appendChild(divOverlayT);
            //divOverlayT.appendChild(spanFullText);

            
            

            if (i==3 | i==8){
                class_id_handle('pIIinner_1_3', 'pIIinner_1_4', divC_pIIinner_1_3);
            
            // // class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_2')
            }else if (i==11 | i==12){
                class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_2', divC_pIIinner_1_3);
            
            // class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_4')
            }else{
                class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_4', divC_pIIinner_1_3);
            };

        };

    };

    //});

    // load more btn
    //document.addEventListener("DOMContentLoaded", function (e) {
    const LoadMoreBtn = document.querySelector('.loadMore');
    LoadMoreBtn.addEventListener('click', function() {
        if (13+loadTimes*10 < dataLength & 23+loadTimes*10 <= dataLength){
            addTenChildren(loadTimes);
            loadTimes += 1;
        }else{
            addTenChildren(loadTimes);
            LoadMoreBtn.style.display = 'none';
        }
        
    });
    //});

    function retrieveDataAndLoad(index){
        if (23+10*index <= dataLength & 13+10*index <= dataLength){
            return [{'stitle':stitles.slice(13+10*index, 23+10*index),
                    'img':imgs.slice(13+10*index, 23+10*index)}, 10]
        }else{
            return [{'stitle':stitles.slice(13+10*index, dataLength + 1),
                    'img':imgs.slice(13+10*index, dataLength + 1)}, dataLength - (13+10*index) + 1]
        };
        
    };
    
    
    // clear operation for className or id setting
    function class_id_handle(Class, ID, tag){
        if (Class == 'pIIinner_1_3' & ID == 'pIIinner_1_4'){
            tag.className = Class;
            tag.setAttribute("id", ID);
        }else if (Class == 'pIIinner_1_3 pIIinner_1_2' & ID == 'pIIinner_1_4'){
            tag.className = Class;
            tag.setAttribute("id", ID);
        }else if (Class == 'pIIinner_1_3 pIIinner_1_2' & ID == 'pIIinner_1_2'){
            tag.className = Class;
            tag.setAttribute("id", ID);
        };
        return tag
    };
    
    // ten pictures a pack per call
    function addTenChildren(ind){
        let tempSpotImg = retrieveDataAndLoad(ind)[0];
        let upperBound = retrieveDataAndLoad(ind)[1];
        for (let i = 1; i <= upperBound; i++){
    
            let container = document.querySelector('.pictureII');
            let divC_pIIinner_1_3 = document.createElement('div');
            let imgSpot = document.createElement('img'); // img append
            let divOverlayS = document.createElement('div');
            let imgStar = document.createElement('img');
            let divOverlayT = document.createElement('div'); // stitle append
            //let spanFullText = document.createElement('span');
    
            divOverlayT.className = 'overlayT';
            divOverlayT.textContent = tempSpotImg.stitle[i-1];
            //spanFullText.textContent = tempSpotImg.stitle[i-1];
            imgSpot.src = tempSpotImg.img[i-1];
            imgStar.src = 'star_icon.png';
            divOverlayS.className = 'overlayS';
            //spanFullText.className = 'tooltiptext';

            container.appendChild(divC_pIIinner_1_3);
            divC_pIIinner_1_3.appendChild(imgSpot);
            divC_pIIinner_1_3.appendChild(divOverlayS);
            divOverlayS.appendChild(imgStar);
            divC_pIIinner_1_3.appendChild(divOverlayT);
            //divOverlayT.appendChild(spanFullText);
    
            
    
            // first big img for 1920~1200
            // class_id_handle('pIIinner_1_3', 'pIIinner_1_4')
            if ((i-1)%5==0){
                class_id_handle('pIIinner_1_3', 'pIIinner_1_4', divC_pIIinner_1_3);
            
            // the rest four small img for 1920~1200
            // // class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_2')
            }else if (i%9==0 | i%10==0){
                class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_2', divC_pIIinner_1_3);
            
            // class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_4')
            }else{
                class_id_handle('pIIinner_1_3 pIIinner_1_2', 'pIIinner_1_4', divC_pIIinner_1_3);
            };
    
        };
    
    };

});


// previous hamburger popup menu
// https://www.geeksforgeeks.org/prevention-from-getting-error-by-adding-script-tag-anywhere-using-domcontentloaded-event-listener-of-javascript/
document.addEventListener("DOMContentLoaded", function (e) {
    const dialog = document.getElementById('pleaseShowUp');
    const openBurger = document.getElementById('bgImg');
    const closeX = document.getElementById('closeImg');

    // Add event listeners to open and close the dialog
    openBurger.addEventListener('click', function() {
        dialog.show(); // Open the dialog
    });

    closeX.addEventListener('click', function() {
        dialog.close(); // Close the dialog
    });

    // Function to hide the popup menu
    function hidePopupMenu() {
        dialog.close();
    };

    // Add event listener to detect changes in viewport width
    window.addEventListener('resize', function() {
        var windowWidth = window.innerWidth;
        if (windowWidth > 600) {
            hidePopupMenu(); // Hide the popup menu if width exceeds 600px
        }
    });
});
