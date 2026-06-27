name: Post to Threads

on:
  schedule:
    - cron: "0 22 * * *" # JST 07:00
  workflow_dispatch:

permissions:
  contents: write

jobs:
  post:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install requests

      - name: Post to Threads
        env:
          THREADS_USER_ID: ${{ secrets.THREADS_USER_ID }}
          THREADS_ACCESS_TOKEN: ${{ secrets.THREADS_ACCESS_TOKEN }}
        run: python post_threads.py

      - name: Commit updated posts.csv
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add posts.csv
          git diff --cached --quiet || git commit -m "Update posted_at"
          git push
