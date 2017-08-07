<?php
// load XML document
$file = 'cd_catalog.xml';
$bookstore = simplexml_load_file($file);

echo 'Books: ' . $bookstore->count() . '<hr>';

foreach ($bookstore as $book) {
	echo $book->title . '<br>';
	echo $book['url'] . '<br>';
	foreach ($book->author->name as $author){
		echo $author . '<br>';
	}
	echo '<hr>';
}

echo $books->book[1]->author. <'br'>;
