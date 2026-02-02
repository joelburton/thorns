thorns.z5: thorns.inf
	inform -S -D thorns.inf

play: thorns.z5
	frotz thorns.z5

thorns.z3: thorns.inf
	inform -v3 -D thorns.inf

play3: thorns.z3
	frotz thorns.z3

upload: thorns.z5
	curl -o html/index.html -F "story_file=@thorns.z5" https://iplayif.com/api/sitegen
	cd html && surge . lady-of-thorns.surge.sh
	xdg-open https://lady-of-thorns.surge.sh
