# Food Delivery App - Design System

## 1. Color Palette

### Primary Colors
- **Primary Green**: `#2ECC71` - Main CTA, active states
- **Primary Dark Green**: `#27AE60` - Hover states, borders
- **Primary Light Green**: `#D5F4E6` - Backgrounds, subtle accents

### Secondary Colors
- **Orange**: `#FF6B35` - Highlights, promotions, special offers
- **Red**: `#E74C3C` - Alerts, errors, urgent notifications
- **Blue**: `#3498DB` - Info, secondary actions

### Neutral Colors
- **White**: `#FFFFFF` - Primary background
- **Light Gray**: `#F8F9FA` - Card backgrounds, secondary backgrounds
- **Medium Gray**: `#95A5A6` - Secondary text, disabled states
- **Dark Gray**: `#2C3E50` - Primary text, headings
- **Black**: `#1A1A1A` - Darkest text, high contrast

### Semantic Colors
- **Success**: `#27AE60` - Order confirmed, delivery complete
- **Warning**: `#F39C12` - Low stock, delayed delivery
- **Error**: `#E74C3C` - Payment failed, order cancelled
- **Info**: `#3498DB` - New offers, updates

---

## 2. Typography

### Font Family
- **Primary Font**: `Segoe UI, Tahoma, Geneva, Verdana, sans-serif`
- **Fallback**: System fonts for cross-platform consistency

### Font Sizes & Scale
| Name | Size | Weight | Line Height | Usage |
|------|------|--------|-------------|-------|
| **H1** | 32px | 700 (Bold) | 40px | Page titles |
| **H2** | 24px | 700 (Bold) | 32px | Section headers |
| **H3** | 20px | 600 (SemiBold) | 28px | Subsection headers |
| **Body Large** | 16px | 400 (Regular) | 24px | Primary content |
| **Body Regular** | 14px | 400 (Regular) | 20px | General text |
| **Body Small** | 12px | 400 (Regular) | 18px | Secondary info, labels |
| **Caption** | 11px | 500 (Medium) | 16px | Timestamps, hints |
| **Button Text** | 14px | 600 (SemiBold) | 20px | Button labels |

---

## 3. Spacing System

### Base Unit: 8px

| Name | Value | Usage |
|------|-------|-------|
| **XS** | 4px | Micro spacing between elements |
| **S** | 8px | Padding in small components |
| **M** | 16px | Standard padding, margins |
| **L** | 24px | Section spacing |
| **XL** | 32px | Large section spacing |
| **XXL** | 48px | Page-level spacing |

### Padding Guidelines
- **Containers**: 16px (M) or 24px (L)
- **Cards**: 16px (M)
- **Buttons**: 12px (vertical) × 16px (horizontal)
- **Input Fields**: 12px (vertical) × 12px (horizontal)

### Margin Guidelines
- **Elements in a row**: 8px (S) between items
- **Section blocks**: 16px-24px (M-L)
- **Page sections**: 32px (XL) or 48px (XXL)

---

## 4. Buttons

### Button Styles

#### Primary Button (CTA)
```
Background: #2ECC71 (Primary Green)
Text Color: #FFFFFF (White)
Border: None
Padding: 12px 24px
Border Radius: 8px
Font: 14px, SemiBold
Box Shadow: 0px 4px 12px rgba(46, 204, 113, 0.3)
Hover: Background #27AE60
Active: Background #229954, Box Shadow 0px 2px 8px rgba(34, 153, 84, 0.2)
Disabled: Background #BDC3C7, Text #95A5A6, Cursor not-allowed
```

#### Secondary Button
```
Background: #F8F9FA (Light Gray)
Text Color: #2C3E50 (Dark Gray)
Border: 1px solid #E0E0E0
Padding: 12px 24px
Border Radius: 8px
Font: 14px, SemiBold
Hover: Background #E9ECEF, Border #D0D0D0
Active: Background #DDE1E6
```

#### Tertiary Button (Text Only)
```
Background: Transparent
Text Color: #2ECC71 (Primary Green)
Border: None
Padding: 12px 24px
Font: 14px, SemiBold
Hover: Background rgba(46, 204, 113, 0.1)
```

#### Icon Button
```
Size: 40px × 40px
Border Radius: 50% or 8px
Background: #F8F9FA
Icon Color: #2C3E50
Padding: 8px
Hover: Background #E9ECEF
```

#### Button with Icon + Text
```
Gap between icon and text: 8px
Use Primary button background
Icon size: 20px
Text alignment: Center with icon
```

---

## 5. Card Component

### Card Structure
```
Border Radius: 12px
Background: #FFFFFF
Border: 1px solid #E0E0E0
Box Shadow: 0px 2px 8px rgba(0, 0, 0, 0.04)
Padding: 16px
Hover Shadow: 0px 8px 16px rgba(0, 0, 0, 0.08)
Transition: all 0.3s ease-in-out
```

### Card Variants

#### Restaurant Card
```
Image Height: 180px (16:9 aspect ratio)
Content Padding: 16px
Title: H3 (20px, Bold)
Sub Title: Body Small (12px, Medium Gray)
Rating: 14px, with icon
Distance: 12px, Medium Gray
Delivery Time: 12px, Medium Gray
Border Radius: 12px
Hover: Scale 1.02, Shadow elevation
```

#### Food Item Card
```
Image Height: 160px
Content Padding: 12px
Title: Body Large (14px, Bold)
Description: 12px, Medium Gray, single line
Price: 16px, Bold, Green
Add Button: Icon button (+ icon) on bottom right
```

#### Order Status Card
```
Order ID: Caption, Medium Gray
Status Badge: 11px, with color coding
Items Count: Small text
Total Price: 16px, Bold
CTA Button: 12px × 24px padding
```

---

## 6. Input Fields

### Input Field Style
```
Height: 48px
Padding: 12px 14px
Border: 1px solid #E0E0E0
Border Radius: 8px
Background: #FFFFFF
Font: Body Regular (14px)
Font Color: #2C3E50
Placeholder Color: #95A5A6
Transition: all 0.2s ease

Focus State:
  Border Color: #2ECC71
  Box Shadow: 0px 0px 0px 3px rgba(46, 204, 113, 0.1)
  Outline: None

Error State:
  Border Color: #E74C3C
  Background: rgba(231, 76, 60, 0.05)
  Error Message: 12px, Red, appears below

Disabled State:
  Background: #F8F9FA
  Border Color: #E0E0E0
  Text Color: #95A5A6
  Cursor: not-allowed

Filled State:
  Border Color: #2ECC71 (subtle)
```

### Input Variations

#### Text Input
```
Type: text, email, phone
Max Width: 100% or set based on context
```

#### Search Input
```
Prefix Icon: Search icon (16px)
Placeholder: "Search restaurants, dishes..."
Clear Icon: X button on right (only when filled)
Padding Left: 40px (icon space)
```

#### Number Input (Quantity)
```
Default: 1
Min: 1
Increment/Decrement: +/- buttons
Width: 100px-120px
```

#### Textarea
```
Height: 120px minimum
Resize: vertical
Padding: 12px 14px
```

#### Select Dropdown
```
Height: 48px
Padding: 12px 14px
Dropdown Icon: Right aligned
Apply same focus/error states as text input
```

---

## 7. UX Rules

### Navigation & Hierarchy
1. **Primary Action**: Always prominent, green button, top/center position
2. **Secondary Actions**: Gray button or link, right of primary
3. **Tertiary Actions**: Text only, subtle color
4. **Destructive Actions**: Red/warning color
5. **Mobile**: Stack buttons vertically when width < 480px

### Feedback & Feedback
1. **Immediate Visual Feedback**: All interactive elements should have hover/active states
2. **Loading States**: Show spinner for >500ms operations
3. **Toast Notifications**: 
   - Success: Green + checkmark, auto-dismiss after 3s
   - Error: Red + alert icon, persist until dismissed
   - Info: Blue, auto-dismiss after 3s
4. **Confirmation Dialogs**: Use for destructive actions (delete, cancel order)

### Forms & Validation
1. **Labels**: Always present, 12px Medium Gray, positioned above or inside field
2. **Required Fields**: Mark with red asterisk (*)
3. **Inline Validation**: Show error as user types (debounce 500ms)
4. **Error Messages**: 12px Red text, below field, icon + message
5. **Success Feedback**: Green checkmark inside field when valid
6. **Disabled Submit**: Disable primary button until form is valid

### Spacing & Alignment
1. **Horizontal Spacing**: 16px (M) between content columns
2. **Vertical Spacing**: Consistent 16px-24px between sections
3. **Card Grids**: 
   - Desktop (>1024px): 3-4 columns
   - Tablet (768-1024px): 2-3 columns
   - Mobile (<768px): 1-2 columns
4. **Container Max Width**: 1200px

### Accessibility
1. **Color Contrast**: WCAG AA minimum (4.5:1 for text)
2. **Focus States**: Always visible (2px outline or highlight)
3. **Icons + Text**: Use both for important actions
4. **Font Size**: Minimum 14px for body text
5. **Touch Targets**: Minimum 44×44px for mobile
6. **Alt Text**: All images must have descriptive alt text

### Loading & Empty States
1. **Loading Skeleton**: Show during data fetch (< 2 seconds)
2. **Empty State**: 
   - Icon: 64px, centered
   - Message: 16px, Dark Gray
   - Sub-message: 14px, Medium Gray
   - CTA Button: Primary button directive
3. **Error State**: Similar to empty, with retry button

### Motion & Animations
1. **Transitions**: 0.2-0.3s for UI elements
2. **Page Transitions**: Fade (200ms)
3. **Loading Animation**: Smooth spinner, 1s rotation
4. **Micro-interactions**: Subtle (scale, opacity), not distracting
5. **Reduce Motion**: Respect `prefers-reduced-motion` media query

### Responsive Design
1. **Breakpoints**:
   - Mobile: < 480px
   - Tablet: 480px - 768px
   - Desktop: 768px - 1024px
   - Large Desktop: > 1024px

2. **Mobile First Approach**: Design for mobile, enhance for larger screens
3. **Text Size**: Increase by 10-15% on large screens
4. **Touch Padding**: Increase from 48px desktop to 56px mobile
5. **Modal Width**: 100vw on mobile (full screen), 600px on desktop

### Onboarding & Guidance
1. **First-time Users**: Highlight key features with subtle badges
2. **Tooltips**: 12px text, dark background, light text, max 100 chars
3. **Tutorials**: Max 3 steps, skip option always available
4. **Contextual Help**: Help icon (?) with INFO badge

### Performance & Best Practices
1. **Images**: Optimize for web, use WebP with fallbacks
2. **Lazy Loading**: Load images below the fold
3. **Animations**: Use GPU-accelerated transforms
4. **Debouncing**: Search (300ms), filters (500ms)
5. **Caching**: Store user preferences locally

---

## 8. Implementation Checklist

- [ ] Define color variables in CSS/SCSS
- [ ] Create typography scale
- [ ] Build spacing utilities
- [ ] Component library for buttons, cards, inputs
- [ ] Responsive breakpoints configured
- [ ] Accessibility audit completed
- [ ] Test on multiple devices and browsers
- [ ] Document design decisions
- [ ] Create Figma/design tool specs
