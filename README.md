# Cam Scanner  
It is an doc scanner which can crop and save the document, document can be uploaded or click at the  
moment. After finding document in the image, it return the image of document.  
## Requirement  
1)It is made on python version 3.8.3
2) opencv version 4.0.1
3) numpy  
## Problems during project  
biggest problem during the project is to find the best values for canny edge detection.  
To solve this I used the median or mean(according to performance) of whole image and  
apply morphological dilation on the result of canny edge detection for error correction.
