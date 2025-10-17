# GitHub Pages Setup Guide

This guide will help you publish your Integrative Oncology Services Dataset website to GitHub Pages.

## Prerequisites

- A GitHub account
- Git installed on your computer
- Basic knowledge of Git commands

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name your repository: `cancer-oncology`
4. Add a description: "Dataset of Integrative Oncology and Wellness Services in Australian Cities"
5. Choose "Public" (required for free GitHub Pages)
6. **Do NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Initialize Git and Push Your Code

Open a terminal in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Add Integrative Oncology Services Dataset website"

# Add your GitHub repository as remote
git remote add origin https://github.com/afzal0/cancer-oncology.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll down to "Pages" section in the left sidebar
4. Under "Source", select "Deploy from a branch"
5. Under "Branch", select `main` and `/ (root)`
6. Click "Save"

## Step 4: Wait for Deployment

GitHub Pages will take a few minutes to build and deploy your site. You'll see a message like:

```
Your site is ready to be published at https://afzal0.github.io/cancer-oncology/
```

## Step 5: Update README.md

Once your site is published, update the URLs in README.md:

The README.md has already been updated with the correct GitHub Pages URL.

## Step 6: Verify Your Website

1. Visit your site at: `https://afzal0.github.io/cancer-oncology/`
2. Test all navigation links
3. Download the data files to ensure they work
4. Check the documentation page

## Custom Domain (Optional)

If you want to use a custom domain:

1. Buy a domain name
2. In your repository settings, under "Pages", add your custom domain
3. Update your domain's DNS settings to point to GitHub Pages
4. Wait for DNS propagation (can take up to 24 hours)

## Updating Your Site

Whenever you make changes:

```bash
# Make your changes, then:
git add .
git commit -m "Description of changes"
git push
```

GitHub Pages will automatically rebuild your site within a few minutes.

## Troubleshooting

### Site Not Showing Up

- Wait 5-10 minutes after enabling GitHub Pages
- Check that your repository is public
- Ensure `index.html` is in the root directory
- Check the "Actions" tab for build errors

### CSS Not Loading

- Check that the CSS path in `index.html` is correct: `css/style.css`
- Clear your browser cache

### Data Files Not Downloading

- Ensure data files are committed and pushed to the repository
- Check file paths in `index.html`

## File Structure

Your repository should have this structure:

```
cancer-oncology/
├── index.html              # Main landing page
├── README.md              # Repository documentation
├── LICENSE                # CC BY 4.0 license
├── _config.yml            # GitHub Pages configuration
├── .gitignore            # Git ignore rules
├── SETUP.md              # This file
├── paper-template.docx    # Original paper document
├── Data_final_cleaned.xlsx # Original data file
├── css/
│   └── style.css         # Stylesheet
├── data/
│   └── integrative_oncology_services.csv  # CSV version of data
└── docs/
    └── documentation.html  # Data documentation page
```

## Need Help?

- GitHub Pages Documentation: https://docs.github.com/en/pages
- GitHub Community Forum: https://github.community/
- Contact the corresponding author: David.taniar@monash.edu

## Next Steps

After setup:

1. Share your website URL with collaborators
2. Submit the data article to *Data in Brief*
3. Update the dataset DOI in the paper once assigned
4. Monitor GitHub Issues for user feedback
5. Plan periodic data updates

---

**Note:** All URLs and references have been configured for the repository at https://github.com/afzal0/cancer-oncology
