FULL_DEBUG = '$$\#FULL_DEBUG'

%.z5: %.inf Makefile
	inform -s -E1 $(if $(NODEBUG),,-D) -S $<

%.z3: %.inf Makefile
	inform  -s '(small.inf)' -v3 -E1 $<
	@echo
	@echo left $$(( (128 * 1024) - $$(wc -c < thorns.z3) ))

%.play: %.z5
	# frotz $<
	killall Gargoyle || echo "not running"
	open -a Gargoyle $<

%.up: %.inf
	pandoc puzzles.md > html/puzzles.html
	pandoc plot.md > html/plot.html
	pandoc style.md > html/style.html
	cp walkthrough.txt html
	inform -E1 -D -S $<
	cp $(<:.inf=).z5 html/
	cd html && surge . lady-of-thorns.surge.sh
	open https://lady-of-thorns.surge.sh
	rm $(<:.inf=).z5

clean:
	rm *.z5 *.html
	inform -S -D thorns.inf

abbrevs:
	rm gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' '(small.inf)' -v3 thorns.inf
	 ../zabbrev/zabbrev-osx -x3 -v3 thorns.inf > abbrevs-z3.inf
	rm gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' -v5 thorns.inf
	 ../zabbrev/zabbrev-osx -x3 -v5 thorns.inf > abbrevs-z5.inf
test:
	@clear; \
	output=$$(inform -E1 $(FULL_DEBUG) -D -S thorns.inf 2>&1); \
	stat=$$?; \
	if [ $$stat -ne 0 ] || echo "$$output" | grep -q "Warning"; then \
		echo "$$output"; \
		echo ""; \
		first_issue=$$(echo "$$output" | grep -E "(Error|Warning):" | head -1 | sed -E 's/^([^(]+)\(([0-9]+)\).*/\1:\2/'); \
		if [ -n "$$first_issue" ]; then \
			code -g "$$first_issue"; \
		fi; \
	else \
		frotz_ctrlc thorns.z5; \
	fi

.PHONY: playtest
playtest:
	inform -E1 -D -S thorns.inf
	open -a Gargoyle thorns.z5

check-hints:
	@ggrep -oP '(?<=^Option )\w+' game_hints.inf | while read id; do \
		ggrep -qi "$$id" thorns.inf || echo "Not found: $$id"; \
	done