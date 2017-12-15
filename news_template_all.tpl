<html>
<head>
<meta charset="utf-8">
</head>
<body>
<a href="/update_news">I Wanna more HACKER NEWS!</a>
<table border=1>
    <tr>
        <th>Title</th>
        <th>Author</th>
        <th>#likes</th>
        <th>#comments</th>
        <th colspan="3">Label</th>
    </tr>
    %for row in rows:
        <tr>
            <td><a href="{{row.url}}">{{row.title}}</a></td>
            <td>{{row.author}}</td>
            <td>{{row.points}}</td>
            <td>{{row.comments}}</td>
            <td>{{row.label}}</td>
		</tr>
    %end
</table>
</body>