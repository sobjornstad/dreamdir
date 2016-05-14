#1/bin/bash
# %%% Prompt the user to add titles to dreams that don't currently have them.

warnedSkip=0
autoHeaders=1

echo "Dreamdir title addition script. Type ? at the prompt for help."
for file in $(ls *.dre)
do
	if ! grep -q "Title:	" "$file"; then
		while :
		do
			warnedSkip=0
			echo -e "\e[1;31m$file\e[0m"
			[ $autoHeaders == 1 ] && dr dump-headers $file
			read -p "Title or [@\$#?]: " newtitle
			case $newtitle in
			"#")
				if [ $autoHeaders == 1 ]; then
					autoHeaders=0
					echo "Automatic header display turned off."
				else
					autoHeaders=1
					echo "Automatic header display turned on."
				fi
				;;
			"@")
				dr cat $file
				;;
			"$")
				dr edit $file
				;;
			"?")
				cat <<-END_MSG
				[1;34mHELP:[0m
				[1;34m#:[0m Turn on/off automatic header display
				[1;34m@:[0m Print dream
				[1;34m$:[0m Open dream in editor
				[1;34m?:[0m Show this help screen
				[1;34m^C:[0m Quit
				
				END_MSG
				;;
			*)
				ed "$file" <<-EOF
				/Date:	
				a
				Title:	$newtitle
				.
				wq
				
				EOF
				break
				;;
			esac
		done

	else # i.e. if $file contains a title header already
		if [ $warnedSkip == 0 ]; then
			echo "!!!!!!!!!! Skipped one or more dreams. !!!!!!!!!!!"
			read -p '(Press Return to continue)'
			warnedSkip=1
		fi
	fi
done
