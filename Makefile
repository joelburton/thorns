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

html: unit
	pandoc -s docs/puzzles.md > html/puzzles.html
	pandoc -s docs/plot.md > html/plot.html
	pandoc -s docs/style.md > html/style.html
	pandoc -s docs/help.md > html/help.html
	cp walkthrough.txt html
	tail +8 thorns.scr |  awk -f scripts/tidy.awk | python3 scripts/transcript_to_html.py > html/final.html
	# inform -E1 -D -S $<
	cp thorns.z5 html/

surge: html
	cd html && surge . lady-of-thorns.surge.sh
	open https://lady-of-thorns.surge.sh
	rm thorns.z5

abbrevs:
	rm gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' '(small.inf)' -v3 thorns.inf
	 ../zabbrev/zabbrev-osx -x3 -v3 thorns.inf > abbrevs-z3.inf
	rm gametext.txt
	inform -r '$$TRANSCRIPT_FORMAT=1' -v5 thorns.inf
	 ../zabbrev/zabbrev-osx -x3 -v5 thorns.inf > abbrevs-z5.inf
	rm gametext.txt

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

.PHONY: walkthrough
walkthrough:
	cat walkthrough/1[a-z]-*.txt > walkthrough/1-start.txt
	cat walkthrough/2[a-z]-*.txt > walkthrough/2-initial-investigate.txt
	cat walkthrough/3[a-z]-*.txt > walkthrough/3-puzzles-east.txt
	cat walkthrough/4[a-z]-*.txt > walkthrough/4-upper.txt
	cat walkthrough/5[a-z]-*.txt > walkthrough/5-crypts.txt
	cat walkthrough/6[a-z]-*.txt > walkthrough/6-belltower-solar.txt
	cat walkthrough/7[a-z]-*.txt > walkthrough/7-undercroft.txt
	cat walkthrough/8[a-z]-*.txt > walkthrough/8-endings.txt
	cd walkthrough && cat 1-* 2-* 3-* 4-* 5-* 6-* 7-* 8-* > 18-combo.txt
	cat walkthrough/18-combo.txt \
	| fgrep -v 'GOTO' \
	> walkthrough.txt
	cp walkthrough.txt walkthrough.rec

.PHONY: playtest
playtest:
	rm -f final.txt
	inform -E1 -D -S thorns.inf
	open -a Gargoyle thorns.z5

check-hints:
	@ggrep -oP '(?<=^Option )\w+' game_hints.inf | while read id; do \
		ggrep -qi "$$id" thorns.inf || echo "Not found: $$id"; \
	done

unit: walkthrough
	rm -f thorns.scr
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
		echo "\nREPLAY\nwalkthrough\n" | dfrotz -S1000 -m -p thorns.z5; \
		awk -f scripts/test.awk thorns.scr && diff -u3 --color=always unit-walkthrough.scr thorns.scr && echo -e "\n\n*** MATCHES"; \
	fi

clean:
	rm -f just_hints.z5 thorns.z3 thorns.z5 walkthrough.rec walkthrough.txt thorns.scr
	cd html && rm -f final.html plans.html plot.html puzzles.html style.html thorns.z5 walkthrough.txt

apple2:
	scp thorns.z3 lab:FictionTools/myproject.z3
	ssh lab "cd FictionTools; source .punyrc; APPLE2_Z3_INFOCOM=true puny -b apple2"
	scp lab:FictionTools/myproject_apple2.dsk /tmp
	open /tmp/myproject_apple2.dsk