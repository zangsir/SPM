/******************************************************************************
*******************************************************************************
******                                                                  *******
******     This code is written by Abdullah Al Mueen at the department  *******
******     of Computer Science and Engineering of University of         *******
******     California - RIverside.                                      *******
******                                                                  *******
*******************************************************************************
******************************************************************************/

/*#############################################################################
######                                                                  #######
######     This code is open to use, reuse and distribute at the user's #######
######     own risk and as long as the above credit is ON. The complete #######
######     description of the algorithm and methods applied can be      #######
######     found in the paper - EXACT DISCOVERY OF TIME SERIES MOTIFS   #######
######     by Abdullah Mueen, Eamonn Keogh and Qiang Zhu.               #######
######                                                                  #######
#############################################################################*/







#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <signal.h>

#define INF 999999999999.0

FILE *fp;
int ref;

double **data;
double **dref;
double **indices;
long long *ind;
long long loc1 , loc2;

double *stdRef;
long long TIMESERIES;
int LENGTH;
int MAXREF;
double bsf;
    
/* Calculates the distance between two time series x and y. If the distance is
larger than the best so far (bsf) it stops computing and returns the approximate
distance. To get exact distance the bsf argument should be omitted.*/

double distance(double *x, double *y, int length , double best_so_far = INF )
{
    int i;
    double sum = 0;
    double bsf2 = best_so_far*best_so_far;
    for ( i = 0 ; i < length && sum < bsf2 ; i++ )
        sum += (x[i]-y[i])*(x[i]-y[i]);
    return sqrt(sum);
    }

/*Comparison function for qsort function. Compares two time series by using their
distances from the reference time series. */

int comp1(const void *a,const void *b)
{
    long long *x=(long long *)a;
    long long *y=(long long *)b;

    if (indices[ref][*x]>indices[ref][*y])
        return 1;
    else if (indices[ref][*x]<indices[ref][*y])
        return -1;
    else
        return 0;
    }


int comp2(const void *a,const void *b)
{
    int *x=(int *)a;
    int *y=(int *)b;

    if (stdRef[*x]<stdRef[*y])
        return 1;
    else if (stdRef[*x]>stdRef[*y])
        return -1;
    else
        return 0;
    }
    

void error(int id)
{
    if(id==1)
        printf("ERROR : Memory can't be allocated!!!\n\n");
    else if ( id == 2 )
        printf("ERROR : File not Found!!!\n\n");
    else if ( id == 3 )
        printf("ERROR : Can't create Output File!!!\n\n");
    else if ( id == 4 )
        printf("ERROR : Invalid Number of Arguments!!!\n\n");

    exit(1);

    }



void stop_exec(int sig)
{

    printf("Current Motif is (%lld",loc1);
    printf(",%lld)",loc2);
    printf(" and the distance is %lf\n",bsf);
    exit(1);
    }

    
    
int main(  int argc , char *argv[] )
{

    double d;
    long long i , j ;
    long long offset = 0;
    int abandon = 0 ,  r = 0;
    double ex , ex2 , mean, std;
    int *rInd;
    long long length;
    int clear = 0;
    double *cntr;
    double t1,t2;
    int verbos = 0;
    double count = 0;

    /* taking inpput time series from the file in the data array and Normalizing
    them as well. */

    bsf = INF;
    i = 0;
    j = 0;
    ex = ex2 = 0;

    t1 = clock();
    signal(SIGINT,stop_exec);


    if(argc < 5 || argc > 6)
    {
        printf("Invalid number of arguments!!!");
        exit(1);
    }


    fp = fopen(argv[1],"r");
    TIMESERIES = atol(argv[2]);
    LENGTH = atoi(argv[3]);
    MAXREF = atoi(argv[4]);
    if( argc == 6 )
        verbos = atoi(argv[5]);

    if( verbos == 1 )
        printf("\nNumber of Time Series : %lld\nLength of Each Time Series : %d\n\n",TIMESERIES,LENGTH);

    data = (double **)malloc(sizeof(double *)*TIMESERIES);
    ind = (long long *)malloc(sizeof(long long)*TIMESERIES);
    if( data == NULL || ind == NULL )
        error(1);
    data[0] = (double *)malloc(sizeof(double)*LENGTH);
    
   // printf("%ld %ld\n\n",data,data[0]);
    if( data[0] == NULL )
        error(1);

    while(fscanf(fp,"%lf",&d) != EOF && i < TIMESERIES)
    {
        data[i][j] = d;
        ex += d;
        ex2 += d*d;
        if( j == LENGTH - 1 )
        {
            mean = ex = ex/LENGTH;
            ex2 = ex2/LENGTH;
            std = sqrt(ex2-ex*ex);
            for( int k = 0 ; k < LENGTH ; k++ )
                data[i][k] = (data[i][k]-mean)/std;
            ex = ex2 = 0;
            ind[i] = i;
            i++;
            if( i != TIMESERIES )
                data[i] = (double *)malloc(sizeof(double)*LENGTH);
            if( data[i] == NULL )
                error(1);

            j = 0;
        }
        else
            j++;
    }

    fclose(fp);
    
    if(verbos == 1)
        printf("Data Have been Read and Normalized\n\n");

    dref = (double **)malloc(MAXREF*sizeof(double *));
    indices = (double **)malloc(MAXREF*sizeof(double *));
    stdRef = (double *)malloc(MAXREF*sizeof(double));
    cntr = (double *)malloc(MAXREF*sizeof(double));
    rInd = (int *)malloc(MAXREF*sizeof(int));
    
    if ( dref == NULL || indices == NULL || stdRef == NULL || cntr == NULL || rInd == NULL )
        error(1);

    //////////////////////////////////////////////////////////////////////////

    /*Generating the reference time series. Here it is a random time series*/

    srand ( time(NULL) );

    for( r = 0 ; r < MAXREF ; r++ )
    {

        dref[r] = (double *)malloc(sizeof(double)*LENGTH);
        indices[r] = (double *)malloc(sizeof(double)*TIMESERIES);
        if( dref[r] == NULL || indices[r] == NULL )
            error(1);

        long long random_pick = rand() % TIMESERIES;
        for( i = 0 ; i < LENGTH ; i++ )
            dref[r][i] = data[random_pick][i];

        if( verbos == 1 )
            printf("\nThe %lldth Time Series is chosen as %dth reference\n",random_pick,r);

            /*Creating the indices array which is a 2 by TIMESERIES
            sized vector having the indices (to the data array) and distances (from the
            reference time series) in each row.*/


            ex = 0;
            ex2 = 0;
            

            for( i = 0 ; i < TIMESERIES ; i++ )
            {
                if( i == random_pick )
                { indices[r][i] = INF; continue; }
                d = indices[r][i] = distance(data[i],dref[r],LENGTH);
                count = count + 1;
                ex += d;
                ex2 += d*d;
                if ( abs(i - random_pick ) <= clear )  continue;
                if ( d < bsf )
                {
                    bsf = d; loc1 = i; loc2 = random_pick;
                    if(verbos == 1)
                        printf("New best-so-far is %lf and (%lld , %lld) are the new motif pair\n",bsf,loc1,loc2);
                }

            }

            ex = ex/(TIMESERIES-1);
            ex2 = ex2/(TIMESERIES-1);
            std = sqrt(ex2-ex*ex);
            


            rInd[r] = r;
            stdRef[r] = std;
            cntr[r] = 0;
            ////////////////////////////////////////////////////////////////////
  }
  
        if(verbos == 1)
            printf("\nReferences are picked and Dist has been Computed\n\n");

        /*Sort the standard Deviations*/
        qsort(rInd,MAXREF,sizeof(int),comp2);

        ref = rInd[0];

        long long remaining = TIMESERIES;

        /*Sort indices using the distances*/
        qsort(ind,TIMESERIES,sizeof(long long),comp1);
        ///////////////////////////////////


         /*Motif Search loop of the algorithm that finds the motif. The algorithm
        computes the distances between a pair of time series only when it thinks
        them as a potential motif'*/

        if(verbos == 1)
            printf("Orderings have been Computed and Search has begun\n\n");
        offset = 0;
        abandon = 0;
        
        while (!abandon && offset < remaining)
        {
            abandon = 1;
            offset++;

            for(i = 0 ; i < remaining - offset ; i++ )
            {
                long long left = ind[i];
                long long right = ind[i + offset];
                if( abs(left-right) <= clear )
                    continue;

                //According to triangular inequality distances between left and right
                //is obviously greater than lower_bound.
                double lower_bound = 0;
                r = 0;
                do
                {
                    lower_bound = fabs(indices[rInd[r]][right] - indices[rInd[r]][left]);
                    r++;
                }while( r < MAXREF && lower_bound < bsf );


                if (r >= MAXREF && lower_bound < bsf)
                {

                    abandon = 0;
                    count =  count + 1;
                    d = distance( data[left] , data[right] , LENGTH , bsf );
                    signal(SIGINT,SIG_IGN);
                    if (d < bsf )
                    {
                        t2 = clock();
                        bsf = d;
                        loc1 = left;
                        loc2 = right;
                        if(verbos == 1)
                            printf("New best-so-far is %lf and (%lld , %lld) are the new motif pair\n",bsf,loc1,loc2);

                        }
                    signal(SIGINT,stop_exec);
                    }
                }
            }
            
        printf("\n\nFinal Motif is the pair ( %lld",loc1);
        printf(", %lld ) and the Motif distance is %lf\n",loc2,bsf);
        t2 = clock();
        if(verbos == 1)
            printf("\nExecution Time was : %lf seconds\n",(t2-t1)/CLOCKS_PER_SEC);

}
