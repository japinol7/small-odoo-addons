## Odoo addons Examples. 

	Small addons examples of Python programming with the Odoo ERP framework.
    You will need to install Odoo 19.0 to use these examples.

	version: 19.0.1.1.0
    release: v19.1.1.0
	author: Joan A. Pinol
	author_nickname: japinol
	author_gitHub: japinol7
	author_twitter: @japinol
	Python: 3.14
	PostgreSQL v. tested: 18.6


## Older versions

    You can find these addons for Odoo 18.0 in the release: v18.1.0.0
    You can find these addons for Odoo 17.0 in the release: v17.0.1.0
    You can find these addons for Odoo 16.0 in the release: v16.0.1.0


## Odoo new addon: JAP Sales

### New Features

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for user with group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br /> 
  * One letter A within a solid circle. 

* Create an Invoice from Selected Sale Lines.
  * Only visible for user with group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.

* Display a list of all sales orders associated with the customer of the current order.
    * You can see all the orders on this list. 
    * But you can only open an order if you have the right permissions.
<br />


### New icons in order lines

Icon mark to duplicate an order line <br />

<img src="screenshots/icon_1.png" width="60"> <br />

Icon mark to show which lines are duplicated with this feature <br />

<img src="screenshots/icon_2.png" width="60"> <br />


### How it works

Install (Activate) this addon modules: 
* JAP Sales
* JAP Customize Version
<br />

Note: The following addon modules will be automatically installed:
* JAP Addons Config
* JAP Security
<br />

<img src="screenshots/screenshot01.png" width="980"> <br /> <br />

You can check the JAP addons version and configuration <br /> <br />

<img src="screenshots/screenshot02.png" width="980"> <br /> <br />
<img src="screenshots/screenshot03.png" width="980"> <br /> <br />
<img src="screenshots/screenshot04.png" width="980"> <br /> <br />

Activate the 'Role Sales Squad' role for the chosen users <br /> <br />

<img src="screenshots/screenshot05.png" width="980"> <br /> <br />

A Sale or quotation will show a duplicate button for each line <br/>
and an icon mark for a line created by duplication <br /> <br />

<img src="screenshots/screenshot06.png" width="980"> <br /> <br />

#### Wizard that opens with the button 'Create Invoice from Lines' <br />
You can select which lines to add to the new invoice and add an internal note. <br /> <br />

<img src="screenshots/screenshot07.png" width="980"> <br /> <br />

#### Invoice created with the Wizard 'Create Invoice from Selected Lines' <br />
<img src="screenshots/screenshot08.png" width="980"> <br /> <br />

#### Wizard that opens with the button 'Sale orders with the same customer' <br />
It displays a list of all sales orders associated with the customer of the current order. <br />
You can open a sale order from this wizard only if you have the right permissions.<br />
You can also open a second wizard to display the current sale order lines <br />
to help you choose the right order.<br /> <br />

<img src="screenshots/screenshot09.png" width="980"> <br /> <br />
<img src="screenshots/screenshot10.png" width="980"> <br /> <br />

### New features starting with release v19.1.1.0

#### New addon: 'JAP Simple Bulk Server Job'
A Technical addon intended to be used by System Administrators.

This addon allows creating special jobs able to process several records in bulk; 
a batch of N items per cron execution. 

It includes a Wizard to create jobs, views to manage them and a cron to execute the jobs.
* All the menus and views can be accessed from this menu:
Settings -- Technical -- Jap. Addons

<img src="screenshots/screenshot11.png" width="980"> <br /> <br />
<img src="screenshots/screenshot12.png" width="800"> <br /> <br />
<img src="screenshots/screenshot13.png" width="980"> <br /> <br />
<img src="screenshots/screenshot14.png" width="980"> <br /> <br />
<img src="screenshots/screenshot15.png" width="980"> <br /> <br />
<img src="screenshots/screenshot16.png" width="800"> <br /> <br />

.
