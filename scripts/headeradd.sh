#1/bin/bash
# %%% Prompt the user to add titles to dreams that don't currently have them.

warnedSkip=0
autoCat=0

echo "Dreamdir header addition script"
read -p "What header would you like to add to your dreams? " theheader

echo -e "\nType ? at the prompt for help."
for file in $(ls *.dre)
do
	if ! grep -q "$theheader:	" "$file"; then
		while :
		do
			warnedSkip=0
			echo -e "\e[1;31m$file\e[0m"
			if [ $autoCat == 1 ]; then 
                dr cat $file
            else
                dr dump-headers $file
            fi
			read -p "New value for $theheader or [@\$#?]: " newtitle
			case $newtitle in
			"#")
				if [ $autoCat == 1 ]; then
					autoCat=0
					echo "Only headers will be displayed automatically."
				else
					autoCat=1
					echo "Entire dream will be displayed automatically."
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
				[1;34m#:[0m Toggle automatic display of entire dream or just headers
				[1;34m@:[0m Print dream
				[1;34m$:[0m Open dream in editor
				[1;34m?:[0m Show this help screen
				[1;34m^C:[0m Quit
				
				END_MSG
				;;
			*)
				ed "$file" >/dev/null 2>&1 <<-EOF
				/Date:	
				a
				$theheader:	$newtitle
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
