# MagiCard 🃏 Official Repo 

This is a public backup to avoid random shits.

## 🔀 Branches

A typical code flow should be `dev >> test >> staging >> main`. You don't have to follow all the rules because we are not a big company with 30+ developers 😃, but it can be a good practice on how to standarize the git management. Here's an [article](https://dev.to/couchcamote/git-branching-name-convention-cch) about it if you need more information. 

- [`main`](https://github.com/USF-msds-603-2022/2022-product-analytics-group-project-group1): Production branch (stable)
- [`dev`](https://github.com/USF-msds-603-2022/2022-product-analytics-group-project-group1/tree/dev): Development branch with the latest features
- [`test`](): should be used for testing. Currently we don't have this branch.
- [`staging`](): should be used for staging. Currently we don't have this branch.


## ☕️ Developing Policy

- Don't directly push to [`main`](https://github.com/USF-msds-603-2022/2022-product-analytics-group-project-group1) branch. Leave it as a pull request (PR).
- It's okay if you don't want to follow these red tapes. 
- All the developings should start from the [`dev`](https://github.com/USF-msds-603-2022/2022-product-analytics-group-project-group1/tree/dev) branch. For example,
```
$ git checkout -b feature/SDE-<ticket_num>_<description> dev
```
- Where,
  - `ticket_num` is the ticket number like `SDE-00`
  - The description should be a brief summary of the ticket like `_add_login_buttons`
- After developing, the current branch `dev/SDE-<ticket_num>_<description>` should be merged to `dev` by,
```
$ git checkout dev
$ git merge --no-ff feature/SDE-<ticket_num>_<description>
```
- Then push changes to the server.
```
$ git push
```
- The `dev` branch should only be merged to the `main` branch if some other people finished the code review.

## ⛴ Docker


#### 🔨 Local Build without Docker

```bash
$ python app/run.py
```

#### 🚧 Local Build with Docker

Use the following command for building the image.

```bash
$ docker build . -t test-image
```

Run the image on port `5000` with the following command.

```bash
$ docker run -p 5000:5000 test-image
```

Open the following address to checkout the basic setups.

```
http://localhost:5000/
```

