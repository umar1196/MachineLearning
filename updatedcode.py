import mysql.connector as ct
import xlsxwriter
from BioSQL import BioSeqDatabase
from Bio import Entrez
from  Bio import SeqIO
from Bio import Align


def generate_sub_db(user, pasword, query_db_name, descrip, db_name, gene_id, flag, given_database_id):

    '''
      function generates a sub database, retrive records from ncbi
      and return sequences of genes
    '''

    _user = user
    _pasword = pasword
    _db_name = db_name
    _descrip = descrip
    _query_db_name = query_db_name
    _gene_id = gene_id
    _flag = flag
    _given_database_id = given_database_id

    try:

        server = BioSeqDatabase.open_database(driver = 'mysql.connector' , user = _user , passwd = _pasword , host = 'localhost' , db = _db_name)
        db = server.new_database(_query_db_name , description = _descrip)
        print('database created')


        handle = Entrez.efetch(db = 'nuccore' , retmode = 'text' , rettype = 'gb' , id = _gene_id)
        db.load(SeqIO.parse(handle , 'genbank'))
        server.commit()
        print('record saved to database')


        try:

            #retrive seqquence from db
            seq = []
            connect_to_db = ct.connect(user = _user, host = 'localhost', database = _db_name, password = _pasword)
            cursor = connect_to_db.cursor()
            if flag == 'yes': #retrive sequences whose biodatabase id given
                cursor.execute('select b.accession , s.seq from biosequence s left join bioentry b on s.bioentry_id = b.bioentry_id left join biodatabase bio on bio.biodatabase_id = b.biodatabase_id where bio.biodatabase_id = %_given_database_id' %_given_database_id)
                for i,g in cursor:
                    print(i,g)
                record = cursor.fetchall()
                for z in range(len(record)):
                    seq.append(record[z][1])
                print(seq)
            else:
                cursor.execute('select s.seq, b.accession from biosequence s left join bioentry b on s.bioentry_id = b.bioentry_id left join biodatabase bio on bio.biodatabase_id = b.biodatabase_id')
                for i,g in cursor:
                    print(i,g)
                record = cursor.fetchall()
                for z in range(len(record)):
                    seq.append(record[z][1])
            return seq

        except Exception as ee:
            print("database data retrival exception: ", ee)

    except Exception as e:
        print("database data inseration  exception: ", e)




def matrix(seq, file_name,idslist):

    '''
      function takes sequences, result file name and genes id list.find similarity score
      of sequences and form similarity matrix
    '''

    _file_name = file_name

    cache = {}
    row = col =  1
    work_book = xlsxwriter.Workbook(_file_name + '.xlsx')
    work_sheet = work_book.add_worksheet()
    align = Align.PairwiseAligner()

    for s in range(len(seq)):
        work_sheet.write(0 , 0 , 'Gene Id')
        work_sheet.write(0 , col ,idslist[s] )
        work_sheet.write(row , 0 ,idslist[s] )
        row = row + 1
        col = col + 1

        for i in range(len(seq)):
            score = align.score(seq[s],seq[i])
            score =  score/len(seq[s])

            if ((idslist[i],idslist[s]) and (idslist[s],idslist[i])  in cache.keys()):
                score = cache[(idslist[s],idslist[i])]
                work_sheet.write((s+1) ,(i+1) , score)
            else:

                work_sheet.write((s+1) ,(i+1) , score)
                cache.update({(idslist[i],idslist[s]) : score})

    work_book.close()


#taking parameters of function
usr = 'root'
pd = 'abc'
sub_db_name = 'abc'
descrioption = 'abc'
data_base = 'abc'
input_file = 'abc.txt'
flag = 'yes'#no
given_database_id = databaseid

#reading input file
with open(input_file, "r") as input_handle:
	   genes_id = input_handle.read().splitlines()
print(genes_id)

#function calling

sequences = generate_sub_db(usr , pd , sub_db_name , description , database_name , genes_id, flag, given_database_id)
mat = matrix(seq = sequences, file_name = 'xyz' , idslist = genes_id)




