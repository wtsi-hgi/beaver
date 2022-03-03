create user beaver
	identified by 'beaverPass';

grant delete, insert, select, update on beaver.* to beaver;

create table users
(
	user_id int auto_increment,
	user_name varchar(15) not null,
	constraint users_pk
		primary key (user_id)
);

create table `groups`
(
	group_id int auto_increment,
	group_name varchar(30) not null,
	constraint groups_pk
		primary key (group_id)
);

create table images
(
	image_id int auto_increment,
	image_name varchar(60) not null,
	user_id int not null,
	group_id int not null,
	constraint images_pk
		primary key (image_id),
	constraint images_groups_group_id_fk
		foreign key (group_id) references `groups` (group_id),
	constraint images_users_user_id_fk
		foreign key (user_id) references users (user_id)
);

create table image_usage
(
	image_id int not null,
	user_id int not null,
	group_id int not null,
	datetime timestamp default CURRENT_TIMESTAMP not null,
	constraint image_usage_groups_group_id_fk
		foreign key (group_id) references `groups` (group_id),
	constraint image_usage_images_image_id_fk
		foreign key (image_id) references images (image_id),
	constraint image_usage_users_user_id_fk
		foreign key (user_id) references users (user_id)
);

create table jobs
(
	job_id varchar(60) not null,
	image_id int not null,
	status enum('Queued', 'BuildingDefinition', 'DefinitionMade', 'BuildingImage', 'Succeeded', 'Failed') default 'Queued' not null,
	detail text null,
	starttime timestamp null,
	endtime timestamp null,
	constraint jobs_images_image_id_fk
		foreign key (image_id) references images (image_id)
);

create unique index jobs_job_id_uindex
	on jobs (job_id);

alter table jobs
	add constraint jobs_pk
		primary key (job_id);

create table packages
(
	package_id int auto_increment,
	package_name varchar(30) not null,
	package_version varchar(15) null,
	commonly_used boolean default false not null,
	package_type enum('std', 'R', 'py') not null,
	github_filename varchar(30) null,
	constraint packages_pk
		primary key (package_id)
);

create table image_contents
(
	image_id int not null,
	package_id int not null,
	constraint image_contents_images_image_id_fk
		foreign key (image_id) references images (image_id),
	constraint image_contents_packages_package_id_fk
		foreign key (package_id) references packages (package_id)
);

create table github_packages
(
	package_id int auto_increment,
	github_user varchar(30) not null,
	repository_name varchar(30) not null,
	commit_hash varchar(60) null,
	constraint github_packages_pk
		primary key (package_id)
);

create table package_dependencies
(
	package_id int not null,
	dependency_id int not null,
	constraint package_dependencies_packages_package_id_fk
		foreign key (package_id) references packages (package_id),
	constraint package_dependencies_packages_package_id_fk_2
		foreign key (dependency_id) references packages (package_id)
);

create table image_name_adjectives
(
	adjective varchar(30) not null
);

create table image_name_names
(
	name varchar(30) not null
);



