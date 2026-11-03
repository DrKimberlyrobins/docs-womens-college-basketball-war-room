# Live schedule connection

The screenshot's zero-games state is accurate: the repository has no verified provider feed.

The repository now includes a Sportradar NCAA Women's Basketball v8 connector using the documented daily schedule API and a GitHub Actions four-hour refresh. It **requires an active authorized Sportradar subscription** and a repository secret named `SPORTRADAR_API_KEY`.

Set the provider's contracted API base using repository variable `SPORTRADAR_BASE_URL` if different from the default trial endpoint. An unauthorized or missing key makes the workflow fail clearly, without writing incomplete schedules.

No live schedule feed is claimed to be functioning until the key is configured and the scheduled workflow has succeeded. This is a licensed API integration, not scraping. The 2026-11-03 games visible on public CBS and FOX schedules are not copied into production because their publication does not establish redistribution permission.
