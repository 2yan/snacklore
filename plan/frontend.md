# Frontend Templates Documentation (MVP)

This document outlines the MVP frontend templates required for Snacklore, based on the wireframes.

## Template Structure

All templates use Jinja2 templating engine. Templates are placed in the `templates/` directory.

## Base Template

### `base.html`
**Purpose**: Base template with common HTML structure and navigation.

**Components**:
- HTML5 document structure
- Meta tags (charset, viewport)
- CSS includes
- JavaScript includes
- Top navigation (includes `top_nav.html`)
- Flash message display
- Content block for child templates

## Page Templates

### 1. `home.html` (Homepage)
**Route**: `/`
**Wireframe**: `homepage.png`

**Components**:
- Hero/welcome section
- Featured or recent recipes grid
- Search bar
- Browse by country section

**Data Requirements**:
- Recent recipes list
- Popular countries (optional)

**Features**:
- Responsive grid layout
- Recipe cards using `recipe_card.html`

### 2. `recipe_detail.html` (Recipe Page)
**Route**: `/recipe/<recipe_id>`
**Wireframe**: `recipe_page.png`

**Components**:
- Recipe title and main image
- Recipe metadata (country, difficulty, time, servings)
- Ingredients list
- Instructions/steps
- Author name
- Edit button (if user is author)
- Comment section (includes `comment_component.html`)

**Data Requirements**:
- Recipe object
- Ingredients array
- Instructions array
- Comments array
- Author information

**Features**:
- Basic layout matching wireframe
- Comment component integration

### 3. `search.html` (Search Page)
**Route**: `/search`
**Wireframe**: `search_page.png`

**Components**:
- Search bar (with query displayed)
- Filter sidebar:
  - Country filter
  - Category filter
  - Difficulty filter
- Results grid
- Basic pagination (if needed)

**Data Requirements**:
- Search query
- Results array
- Filter options

**Features**:
- Form-based filtering
- Results count display
- Empty state message

### 4. `user_profile.html` (User Profile)
**Route**: `/user/<username>` or `/profile`
**Wireframe**: `user_profile.png`

**Components**:
- User avatar and username
- Bio/description (optional)
- Statistics (recipes count)
- Tabs:
  - My Recipes
  - Favorites (if implemented)
- Recipe grid of user's recipes

**Data Requirements**:
- User object
- Recipes created by user
- User statistics

**Features**:
- Tab navigation
- Recipe cards grid

### 5. `register.html` (User Registration)
**Route**: `/register`
**Wireframe**: `register_user.png`

**Components**:
- Registration form:
  - Username field
  - Email field
  - Password field
  - Confirm password field
- Submit button
- Link to login page
- Error message display

**Data Requirements**:
- Form validation errors

**Features**:
- Basic form validation
- Error display

### 6. `login.html` (User Login)
**Route**: `/login`

**Components**:
- Login form:
  - Username/Email field
  - Password field
- Submit button
- Link to registration page
- Error message display

**Data Requirements**:
- Form validation errors

## Recipe Editor Templates

### 7. `recipe_edit.html` (Text Editor Recipe)
**Route**: `/recipe/<recipe_id>/edit` or `/recipe/new`
**Wireframe**: `text_editor_recipe.png`

**Components**:
- Recipe title input
- Recipe description/notes (textarea)
- Ingredients text area
- Instructions text area
- Metadata fields:
  - Country selection
  - Difficulty level
  - Prep time
  - Cook time
  - Servings
- Image upload (single file)
- Save button
- Cancel button

**Data Requirements**:
- Recipe object (if editing)
- Country list
- Form validation errors

**Features**:
- Basic form validation
- Image upload (single image)

### 8. `recipe_edit_gui.html` (GUI Editor Recipe)
**Route**: `/recipe/<recipe_id>/edit?mode=gui` or `/recipe/new?mode=gui`
**Wireframe**: `gui_editor_recipe.png`

**Components**:
- Recipe title input
- Ingredient builder:
  - Add ingredient button
  - Ingredient rows with:
    - Name field
    - Quantity field
    - Unit dropdown
    - Remove button
- Instruction builder:
  - Add step button
  - Step rows with:
    - Step number
    - Instruction text area
    - Remove button
- Metadata fields (same as text editor)
- Image upload
- Save button
- Cancel button

**Data Requirements**:
- Recipe object (if editing)
- Country list
- Unit options
- Form validation errors

**Features**:
- Add/remove dynamic fields (JavaScript)
- Basic form validation

## Component Templates

### 9. `includes/top_nav.html` (Top Navigation)
**Wireframe**: `top_nav.png`

**Components**:
- Logo/Brand name (links to home)
- Search bar
- Navigation links (Browse, etc.)
- User menu (if logged in):
  - User name
  - Profile link
  - Logout button
- Login/Register buttons (if not logged in)

**Data Requirements**:
- Current user (if logged in)
- Current route (for active state)

**Features**:
- Responsive mobile menu
- Active link highlighting

### 10. `includes/comment_component.html` (Comment Component)
**Wireframe**: `comment_component.png`

**Components**:
- Comment form (if logged in):
  - Comment text area
  - Submit button
- Comments list:
  - Comment card:
    - User name
    - Comment text
    - Timestamp
    - Delete button (if user's comment)

**Data Requirements**:
- Comments array
- Current user (for delete permissions)
- Recipe ID

**Features**:
- Basic comment display
- Delete own comments

### 11. `includes/recipe_card.html` (Recipe Card Component)

**Components**:
- Recipe image thumbnail
- Recipe title
- Country name
- Difficulty indicator
- Time estimate
- Author name

**Data Requirements**:
- Recipe object

**Features**:
- Link to recipe detail page
- Responsive card layout

## Template Organization

```
templates/
├── base.html                    # Base template
├── home.html                    # Homepage
├── recipe_detail.html           # Recipe detail page
├── search.html                  # Search results
├── user_profile.html            # User profile
├── register.html                # Registration
├── login.html                   # Login
├── recipe_edit.html             # Text recipe editor
├── recipe_edit_gui.html         # GUI recipe editor
└── includes/
    ├── top_nav.html             # Top navigation
    ├── comment_component.html   # Comment component
    └── recipe_card.html         # Recipe card
```

## MVP Features

### Essential Features
- Responsive design (mobile-friendly)
- Basic form validation
- Flash messages for user feedback
- Image upload (single image per recipe)
- Search and filter functionality
- User authentication (login/register)

### Out of Scope for MVP
- Auto-save drafts
- Drag-and-drop reordering
- Nested comments
- Social sharing
- Favorites system (can be added later)
- Advanced filtering
- Real-time search
- Image upload per step
- Markdown support
- Password strength indicators
- Settings page
- Country detail pages

## Data Flow

1. Routes (`app.py`) → Fetch data from database
2. Routes → Pass data to templates via `render_template()`
3. Templates → Display data using Jinja2
4. Templates → Include reusable components
5. Base template → Provides common structure

## JavaScript Requirements (MVP)

- Form validation (client-side)
- Dynamic form fields (add/remove ingredients/steps in GUI editor)
- Image upload handling
- Basic AJAX for comments (optional)

