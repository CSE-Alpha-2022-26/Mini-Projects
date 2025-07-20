# 📌 Pull Request Description

## 🎯 Purpose of Changes
<!-- Clearly explain what problem this solves or what feature it adds -->
**Example:**  
"This PR implements user authentication for the EcoTrack project, allowing:  
- Secure login/logout functionality  
- JWT token generation  
- Protected API routes"

## 🔗 Related Resources
| Type | Link |  
|------|------|  
| Issue | Fixes #123 |  
| Design | [Figma Prototype](url) |  
| Docs | [API Spec](url) |  

## 🧪 Testing Performed
<!-- Detail how you verified your changes work -->
```gherkin
Scenario: User Login
  Given I'm on /login page
  When I enter valid credentials
  Then I should see dashboard
  And receive JWT cookie
```

## 📸 Visual Evidence
| Before | After |  
|--------|-------|  
| ![Old Login](https://via.placeholder.com/300x200?text=No+Auth) | ![New Login](https://via.placeholder.com/300x200?text=Secure+Login) |  

## ✅ Compliance Checklist
- [ ] **Code Quality**  
  - [ ] Linting passes (`npm run lint`)  
  - [ ] No console.log statements  
- [ ] **Testing**  
  - [ ] Unit tests added  
  - [ ] Integration tests pass  
- [ ] **Documentation**  
  - [ ] README updated  
  - [ ] API docs generated  
- [ ] **Style Guide**  
  - [ ] Follows [PEP8](https://peps.python.org/pep-0008/)  
  - [ ] Consistent indentation  

## 🚧 Known Issues
<!-- List any limitations or TODOs -->
1. Password reset not yet implemented  
2. Mobile responsiveness needs improvement  

## 💡 Recommended Review Focus
<!-- Guide reviewers to critical changes -->
1. `src/auth/jwt.service.ts` - Token generation logic  
2. `tests/auth.spec.js` - Test coverage  

## ⚙️ Deployment Notes
```bash
# New environment variables required
AUTH_SECRET=your_secret_key
TOKEN_EXPIRY=24h
```

---

### Why This Improves Your Process:
1. **Structured Testing Documentation** - Clear BDD format shows verification steps
2. **Visual Change Tracking** - Before/after screenshots help reviewers
3. **Targeted Review Guidance** - Saves time by highlighting critical files
4. **Compliance Tracking** - Organized checklist ensures nothing's missed
5. **Future Reference** - Deployment notes aid maintenance
