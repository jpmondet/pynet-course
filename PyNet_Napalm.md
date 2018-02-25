David Barroso and Elisa Jasinska recently created a library called NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support). The general idea behind this library is to create a standardized, multivendor interface for certain file and get operations. Last fall, Gabriele Gerbino added Cisco IOS support to NAPALM.


Independent of NAPALM, I have been thinking about and experimenting with programmatic file operations using Cisco IOS. I wrote a proof of concept related to this here. Consequently, I thought it made sense to add/improve the Cisco IOS file operations in NAPALM. Because of this, I re-wrote the file methods in the NAPALM Cisco IOS driver (sorry about that Gabriele). Basically, I thought using secure copy (SCP), 'configure replace', and a file-based configuration merge (copy file system:running-config) would be more consistent with NAPALM and ultimately provide a better solution (in the context of NAPALM file operations).
So what can you do with NAPALM in the context of Cisco IOS?

    Configuration replace: replace the entire running-config with a completely new configuration.
    Configuration merge: merge a set of changes from a file into the running-config.
    Configuration compare: compare your new proposed configuration file with the running-config. This only applies to configuration replace operations; it does not apply to merge operations.
    Commit: deploy the staged configuration. This can be either an entire new file (for replace operations) or a merge file.
    Discard: revert the candidate configuration file back to the current running-config; reset the merge configuration file back to an empty file.
    Rollback: revert the running configuration back to a file that was saved prior to the previous commit.
     


​But what happens under the hood?


Under the hood, there are three files that can potentially be used: 'candidate_config.txt', 'merge_config.txt', and 'rollback_config.txt'. The default file system is 'flash:', but this default can be overridden.

For configure replace operations, the new config file will be secure copied to 'candidate_config.txt'. Upon commit, Cisco's 'configure replace' command will be executed (see here for details).

Similarly, a merge operation will SCP a file to 'flash:/merge_config.txt'. Upon commit, a 'copy flash:merge_config.txt system:running-config' command will be executed (once again a different file system can be used and 'flash:' is not required).

Compare configuration will perform a diff between the candidate_config.txt file and the running-config using 'show archive config differences'.

Finally, the discard and rollback commands will manipulate the three files ('candidate_config.txt', 'merge_config.txt', 'rollback_config.txt'). Discard config will cause the current running-config file to be copied into candidate_config.txt. Additionally, discard config will cause the merge_config.txt file to be zeroed out. The rollback command will cause the 'rollback_config.txt' file to become the running-config (once again using Cisco's 'configure replace' command). Note, the current running-config is saved to rollback_config.txt on any commit operation.


For additional details, including examples, see:

https://pynet.twb-tech.com/blog/automation/napalm-ios.html

