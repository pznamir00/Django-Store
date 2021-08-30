<h1>Django Clothes Store Project</h1>
<hr/>
<p>
    Simple project of online shop backend builded with Python Django.<br/>
    Application contains auth system, product management and order system.<br/>
    This is base backend project for this kind of online store that you can use and extend.<br/>
</p>
<br/>
<br/>
<h3>ENDPOINTS:</h3>
<hr/>
<h4>Auth:</h4>
<ul>
    <li>
        <b>api/auth/user/</b><br/>
        - get data of logged user (for logged)
    </li>
    <li>
        <b>api/auth/login/</b><br/>
        - login<br/>
        - data: { username, password }
    </li>
    <li>
        <b>api/auth/logout/</b><br/>
        - logout (for logged)
    </li>
    <li>
        <b>api/auth/registration/</b><br/>
        - get data of logged user (for logged)<br/>
        - data: { username, email, password1, password2, phone_number, street, home_number, apartament_number, city, zip_code }
    </li>
    <li>
        <b>api/auth/password/reset/</b><br/>
        - send link with password reset to email (if exists)<br/>
        <b>- requires set frontend url during sending email</b>
    </li>
    <li>
        <b>api/auth/password/reset/confirm/</b><br/>
        - reset password<br/>
        - data: { uid, token, new_password1, new_password2 }
    </li>
</ul>

<h4>Products:</h4>
<ul>
    <li>
        <b>api/products/ CRUD</b><br/>
        - All methods for Product model<br/>
        - Allows for view for ordinary user, only admin can edit data
        - create/update - data:<br/>
        { name, description, price, color, brand, subcategory, sizes([ { size(id), quantity }, ... ]), <br/>
        base64files([ file1, file2, file3 ... ] (files encoded in base64)) }
    </li>
    <li>
        <b>api/sizes/ CRUD</b><br/>
        - All methods for Size model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
</ul>

<h4>Orders:</h4>
<ul>
    <li>
        <b>api/cart/</b><br/>
        - get products in cart<br/>
        - data: { products: [ { product_size_relation, quantity }, ... ] }<br/>
        - client must save id of selected products and can get and valid them in this route<br/>
        - <b>product_size_relation</b> - id of SizeProductRelation object which indicates on selected product and size
    </li>
    <li>
        <b>api/products/ CRUD</b><br/>
        - All methods for Product model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
    <li>
        <b>api/orders/ CRUD</b><br/>
        - list returns empty array or orders list of logged user unless logged user is admin, in this case - all data<br/>
        - no update<br/>
        - destroy only for admin<br/>
        - create for all users - data: <br./>
        { cart (as above), street, home_number, apartament_number, city, zip_code, phone_number, payment_method, <br/>
        shipping_method, discount_code(optional) }
    </li>
</ul>

<hr/>
<h4>Others:</h4>
<h5>Categories:</h5>
<ul>
    <li>
        <b>api/categories/ CRUD</b><br/>
        - All methods for Category model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
    <li>
        <b>api/subcategories/ CRUD</b><br/>
        - All methods for SubCategory model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
</ul>

<h5>Brands:</h5>
<ul>
    <li>
        <b>api/brands/ CRUD</b><br/>
        - All methods for Brand model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
</ul>

<h5>Colors:</h5>
<ul>
    <li>
        <b>api/colors/ CRUD</b><br/>
        - All methods for Color model<br/>
        - Allows for view for ordinary user, only admin can edit data
    </li>
</ul>


<hr/>
<h1>Packages:</h1>
<ul>
    <li>Django</li>
    <li>Django REST Framework</li>
    <li>Django CORS Headers</li>
    <li>Dj_rest_auth</li>
    <li>Allauth</li>
    <li>Colorfield</li>
    <li>Django Filters</li>
    <li>Django Cleanup</li>
    <li>Phonenumber Field</li>
</ul>
