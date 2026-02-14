%.z5: %.inf thints.h
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

%.up: %.inf
	inform -E1 +lib -S $<
	cp $(<:.inf=).z5 html/
	cd html && surge . lady-of-thorns.surge.sh
	open https://lady-of-thorns.surge.sh
	rm $(<:.inf=).z5

clean:
	rm *.z5 *.html
	inform -S -D thorns.inf

test:
	@clear; \
	output=$$(inform -E1 -D -S thorns.inf 2>&1); \
	stat=$$?; \
	if [ $$stat -ne 0 ] || echo "$$output" | grep -q "Warning"; then \
		echo "$$output"; \
		echo ""; \
		first_issue=$$(echo "$$output" | grep -E "(Error|Warning):" | head -1 | sed -E 's/^([^(]+)\(([0-9]+)\).*/\1:\2/'); \
		if [ -n "$$first_issue" ]; then \
			code -g "$$first_issue"; \
		fi; \
	else \
		./frotz thorns.z5; \
	fi
