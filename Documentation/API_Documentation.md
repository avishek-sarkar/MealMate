# MealMate API Documentation

This document lists the HTTP endpoints exposed by the MealMate Flask application.

## Authentication

| Endpoint | Methods | Description |
| --- | --- | --- |
| /register | POST | Student registration |
| /register-hotel | POST | Hotel owner registration |
| /login | POST | User or hotel owner login |
| /logout | GET, POST | Logout current session |
| /admin/login | GET, POST | Admin login |
| /admin/logout | GET, POST | Admin logout |

## Content and Interactions

| Endpoint | Methods | Description |
| --- | --- | --- |
| /api/posts | GET | Feed of reviews and posts |
| /api/hotels | GET | List approved hotels |
| /api/homemade-food | GET | List homemade food posts |
| /api/menu-items/<hotel_id> | GET | Menu items for a hotel |
| /api/notifications | GET | User notifications |
| /api/post/like | POST | Like or unlike a post |
| /api/post/comment | POST | Comment on a post |
| /api/post/interactions/<post_id>/<post_type> | GET | Interaction counts |
| /post-review | POST | Submit a review |
| /post-food | POST | Submit a homemade food post |
| /cleanup-expired | POST | Manually purge expired content |

## Hotel Owner Actions

| Endpoint | Methods | Description |
| --- | --- | --- |
| /add-menu-item | POST | Add menu item |
| /delete-menu-item/<item_id> | DELETE | Delete menu item |
| /toggle-menu-availability/<item_id> | PUT | Toggle availability |
| /update-menu-item/<item_id> | PUT | Update menu item |
| /menu-stats | GET | Menu analytics |
| /my-menu | GET | Owner menu items |
| /my-posts | GET | Owner or user posts |

## Profile and Security

| Endpoint | Methods | Description |
| --- | --- | --- |
| /update-profile | PUT, POST | Update user profile |
| /update-business | PUT, POST | Update hotel profile |
| /change-password | PUT, POST | Change student password |
| /change-hotel-password | PUT, POST | Change hotel owner password |
| /get-profile | GET | Current session profile |

## Admin Panel

| Endpoint | Methods | Description |
| --- | --- | --- |
| /admin/dashboard | GET | Admin dashboard |
| /admin/users | GET | Manage users |
| /admin/hotels | GET | Manage hotels |
| /admin/reviews | GET | Manage reviews |
| /admin/food-posts | GET | Manage food posts |
| /admin/approve-user/<user_id> | POST | Approve user |
| /admin/approve-hotel/<hotel_id> | POST | Approve hotel |
| /admin/delete-user/<user_id> | DELETE | Delete user |
| /admin/delete-hotel/<hotel_id> | DELETE | Delete hotel |
| /admin/delete-review/<review_id> | DELETE | Delete review |
| /admin/delete-food-post/<post_id> | DELETE | Delete food post |
