# Simple TODO's

## Description

For my new job as a San Franisco tour guide, I totally realized that I can use the Meteor simple-todos tutorial! It was really easy, the app works perfectly by step 9 of the tutorial, you don't even need to write your own 'publish and subscribe' code! It's all done for you!

https://simple-todos-6c7bf285.challenges.bsidessf.net

The linked tutorial:

* <https://www.meteor.com/tutorials/blaze/creating-an-app>

## Analysis

The app uses mongodb and this page has a hint:

* <https://www.meteor.com/tutorials/blaze/forms-and-events>

"Being able to insert anything into the database from the client isn't very secure, but it's okay for now. In step 10 we'll learn how we can make our app secure and restrict how data is inserted into the database."

This guy skipped step 10, so what did he miss?

* <https://www.meteor.com/tutorials/blaze/publish-and-subscribe>

```
Now that we have moved all of our app's sensitive code into methods, we need to learn about the other half of Meteor's security story. Until now, we have worked assuming the entire database is present on the client, meaning if we call Tasks.find() we will get every task in the collection. That's not good if users of our application want to store privacy-sensitive data. We need a way of controlling which data Meteor sends to the client-side database.

Just like with insecure in the last step, all new Meteor apps start with the autopublish package. Let's remove it and see what happens:

meteor remove autopublish

When the app refreshes, the task list will be empty. Without the autopublish package, we will have to specify explicitly what the server sends to the client.
```

## Solution

Open up burpsuite to see the requests.

Create a user account and add a new task. Using burp proxy to intercept the request there is an interesting websocket message:

```
["{\"msg\":\"method\",\"method\":\"tasks.insert\",\"params\":[\"test\"],\"id\":\"32\",\"randomSeed\":\"972e4000e89c0549ec4c\"}"]
```

And if you refresh the page with the proxy on and walk through each websocket response sent to the client, there it is:

```
a["{\"msg\":\"added\",\"collection\":\"flag\",\"id\":\"guMcsgZYJvW2exh83\",\"fields\":{\"flag\":\"CTF{meteor_js_does_san_francisco}\"}}"]
```

The flag is:

```
CTF{meteor_js_does_san_francisco}
```

