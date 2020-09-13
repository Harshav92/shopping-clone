# Shopping-clone Back-end web services implementation

## Services implemented
* [Register](#register)
* [Login](#login)
* [show products](#show-products)
* 

### Register service
* This service takes five inputs "name" , "email" , "phone_no" ,"password" , "role - [ user/owner/admin ]"
* url_path : /user/register

### Login Service
* takes two inputs "email"/"phone_no" and "password"
* url_path : /user/login
* returns JWT auth string 

### Show products
* Requires auth_code in header
* url_path : /product/show
* Returns list of products in json format
