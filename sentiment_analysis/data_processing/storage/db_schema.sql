-- Table structure for POSTS
-- This table stores reddit submissions data.
-- Columns:
--   id: Unique identifier for each post. ( PRIMARY KEY )
--   TITLE: The title of the post.
--   POST_DATE: The date and time when the post was created in unix format.
--   SCORE: The score or rating of the post.
--   NUM_COMMENTS: The number of comments on the post.
--   UPVOTE_RATIO: The ratio of upvotes to total votes on the post.
--   OVER_18: Indicates if the post is marked as "over 18" content.
--   YEAR: The year of the post creation date.
--   MONTH: The month of the post creation date.
--   DAY: The day of the post creation date.
--   HOUR: The hour of the post creation date.


-- Table structure for COMMENTS
-- This table stores comments data.
-- Columns:
--   id: Unique identifier for each comment. ( PRIMARY KEY )
--   post_id: The id of the post the comment belongs to. ( FOREIGN KEY )
--   body: The content of the comment.
--   date: The date and time when the comment was posted.
--   is_submitter: Indicates if the commenter is the submitter of the post.
--   score: The score or rating of the comment.
--   replies_count: The number of replies to the comment.
--   YEAR: The year of the comment date.
--   MONTH: The month of the comment date.
--   DAY: The day of the comment date.
--   HOUR: The hour of the comment date.


