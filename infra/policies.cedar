// Cedar — Apache-2.0 open-source policy language by AWS.
// Declarative authorization for the demo console: the built-in demo sign-in
// honours this contract; the deploy kit ships the file wherever the stack
// lands. Judge credentials (demo / demo-not-real) are printed in the writeup.

entity User;
entity Console;
action View applies to {Console};

permit(
  principal == pranapath::User::"guest",
  action == pranapath::Action::"View",
  resource == pranapath::Console::"dashboard"
);
