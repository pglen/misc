# Makefile

all:
	@echo "Targets: git clean"

clean:
	rm -f test.txt

git:
	#make clean
	git add .
	git commit -m auto
	git push
	#git push local

# Specific to my system

copy:
	cp -a comalert.py ~/pgbin
