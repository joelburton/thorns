%.z5: %.inf
	inform -E1 +lib -S -D $<

%.play: %.z5
	# frotz $<
	killall Gargoyle || echo "not running"
	open -a Gargoyle $<

%.html_BROKEN: %.z5
	curl -o $@ -F "story_file=@$<" https://iplayif.com/api/sitegen

%.up_BROKEN: %.html
	cp $< html/index.html
	cd html && surge . lady-of-thorns.surge.sh
	open https://lady-of-thorns.surge.sh

%.up: %.z5
	cp $< html/
	cd html && surge . lady-of-thorns.surge.sh
	open https://lady-of-thorns.surge.sh

clean:
	rm *.z5 *.html
	inform -S -D thorns.inf
