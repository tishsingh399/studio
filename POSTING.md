# Posting

Today posting is manual: open `builds/<slug>/post.md`, copy the caption for that account, post `capture.jpg` or `capture.mp4` from your phone.

## What auto-posting through the Instagram Graph API needs

1. Both accounts switched to Professional (Creator or Business) in the Instagram app.
2. Each one linked to a Facebook Page (one Page per account, they can be empty).
3. A Meta developer app with the Instagram Graph API added, and permissions `instagram_basic` and `instagram_content_publish`. Publishing to accounts you own works in development mode, so no app review.
4. A long-lived access token (lasts 60 days, then needs a refresh) and each account's Instagram user ID.
5. Those go in `.env` (copy `.env.example`). `.env` is git-ignored, so the token never lands in this public repo.
6. The capture has to be at a public URL, because the API fetches the file itself rather than taking an upload. A raw GitHub link to `capture.jpg` in this repo works once it's pushed.

Meta also has a newer "Instagram API with Instagram Login" path that skips the Facebook Page. Either works; the Page route is the long-standing one.

Posting is then two calls per account: create a media container with the image URL and caption, then publish it. Videos go up as Reels and take a minute or two to process before they can be published.

## Recommendation

Don't automate yet. Post the first month by hand.

Four posts a month is about ten minutes of copy and paste, and the setup above (two Pages, a Meta app, a token that expires every 60 days) is more work than that. The month by hand also tells you whether the drafts need heavy rewriting. If you are posting them close to as written by the end of the month, automate. If you are rewriting every one, better drafts matter more than a posting bot.
